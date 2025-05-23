import chainlit as cl
from chainlit.input_widget import Select
import requests
import json
import asyncio
import base64

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "gemma3:4b"
SYSTEM_PROMPT = (
  "Your name is Kero. You're a frog who is knowledgeable and helpful."
  "Always provide clear, concise, and accurate answers, with an occasional froggy flair."
  "Do not prefix your answers with 'Assistant:'."
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("conversation_history", [])
    
    # Show dropdown for model selection
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Choose a model",
                values=["gemma3:4b"],
                initial_index=0,
            )
        ]
    ).send()

    selected_model = settings["Model"]
    cl.user_session.set("model_name", selected_model)

    await cl.Message(content=f"Ribbit ribbit ☆.𓋼𓍊 𓆏 𓍊𓋼𓍊.☆").send()


@cl.on_settings_update
async def on_settings_update(settings):
    selected_model = settings["Model"]
    cl.user_session.set("model_name", selected_model)


@cl.on_message
async def on_message(message: cl.Message):
    model = cl.user_session.get("model_name", DEFAULT_MODEL)

    prompt = message.content or "Describe the image."
    images = []

    # Get prior messages for contextual history
    history = cl.user_session.get("conversation_history", [])

    # Process uploaded images
    if message.elements:
        for uploaded_element in message.elements:
            if uploaded_element.mime.startswith("image/"):
                with open(uploaded_element.path, "rb") as f:
                    file_data = f.read()
                b64_image = base64.b64encode(file_data).decode("utf-8")
                images.append(b64_image)

    TOKEN_LIMIT = 128_000

    def estimate_tokens(text):
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4

    # Trim history if over token limit
    def trim_history(history, prompt, limit=TOKEN_LIMIT):
        total_tokens = estimate_tokens(f"User: {prompt}\nAssistant: ")
        trimmed_history = []

        # Iterate through history and add turns until the token limit is exceeded
        for turn in reversed(history):  # Start from the most recent turn
            turn_tokens = estimate_tokens(
                f"User: {turn['prompt']}\nAssistant: {turn['response']}\n"
            )
            if total_tokens + turn_tokens > limit:
                break
            trimmed_history.append(turn)
            total_tokens += turn_tokens

        # Reverse the trimmed history to maintain chronological order
        return list(reversed(trimmed_history))
    # Before building contextual_prompt:
    history = trim_history(history, prompt)

    # Prepend past conversation as prompt
    contextual_prompt = f"{SYSTEM_PROMPT}\n"
    for turn in history:
        contextual_prompt += f"User: {turn['prompt']}\nAssistant: {turn['response']}\n"
    contextual_prompt += f"User: {prompt}\nAssistant: "

    payload = {
        "model": model,
        "prompt": contextual_prompt,
        "stream": True,
    }
    if images:
        payload["images"] = images

    msg = cl.Message(content="")
    await msg.send()

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for line in response.iter_lines():
                if not line:
                    continue
                data = line.decode("utf-8")
                chunk = json.loads(data)
                token = chunk.get("response", "")
                if token:
                    full_response += token
                    await msg.stream_token(token)
                    await asyncio.sleep(0.02)
    except Exception as e:
        await cl.Message(content=f"💥 Error querying `{model}`: {str(e)}").send()
        return

    # Save this turn to memory (session-limited)
    history.append({"prompt": prompt, "response": full_response})
    cl.user_session.set("conversation_history", history)

    await msg.update()
