import chainlit as cl
from chainlit.input_widget import Select
import requests
import json
import asyncio

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma3:4b"

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])

    # Show dropdown for model selection
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Choose a model",
                values=["gemma3:4b", "deepseek-r1:7b"],
                initial_index=0,
            )
        ]
    ).send()

    selected_model = settings["Model"]
    cl.user_session.set("model_name", selected_model)

    await cl.Message(content=f"Hey littlemiss!").send()
    
@cl.on_settings_update
async def on_settings_update(settings):
    selected_model = settings["Model"]
    cl.user_session.set("model_name", selected_model)

@cl.on_message
async def on_message(message: cl.Message):
    model = cl.user_session.get("model_name", DEFAULT_MODEL)
    history = cl.user_session.get("chat_history", [])
    history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    try:
        with requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "messages": history,
                "stream": True
            },
            stream=True
        ) as response:
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines():
                if not line:
                    continue
                data = line.decode("utf-8")
                if data.startswith("data: "):
                    data = data[len("data: "):]
                chunk = json.loads(data)
                token = chunk.get("message", {}).get("content", "")
                if token:
                    full_response += token
                    await msg.stream_token(token)
                    await asyncio.sleep(0.02)

    except Exception as e:
        await cl.Message(content=f"💥 Error querying `{model}`: {str(e)}").send()
        return

    history.append({"role": "assistant", "content": full_response})
    cl.user_session.set("chat_history", history)
    await msg.update()
