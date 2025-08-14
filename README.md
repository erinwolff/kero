# Kero: Chainlit + Ollama Chatbot

Kero is a local chatbot web app built with [Chainlit](https://www.chainlit.io/) and [Ollama](https://ollama.com/), featuring image upload and contextual conversation memory. It uses the `gpt-oss:20b` model by default and runs entirely on your machine.

## Features
- Conversational AI with context memory
- Image upload and vision support
- Model selection dropdown (currently only `gpt-oss:20b`)
- Customizable theme (see `public/theme.json`)
- Local, private, and fast

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) installed and available in your PATH
- (Optional) Python virtual environment

## Installation
1. Clone this repository.
2. (Recommended) Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure Ollama is installed and the `gpt-oss:20b` model is available:
   ```bash
   ollama pull gpt-oss:20b
   ```

## Usage
Run the chatbot with:
```bash
python run_chat.py
```
This will start the Ollama server (if not already running) and launch the Chainlit app.

The web UI will be available at [http://localhost:5000](http://localhost:5000) by default.

## File Overview
- `main.py` — Chainlit app logic (chat, image upload, context, model selection)
- `run_chat.py` — Script to launch Ollama and Chainlit together (on port 5000)
- `requirements.txt` — Python dependencies (`chainlit`, `requests`)
- `public/` — Theme and avatar assets

## Customization
- Edit `public/theme.json` to change the UI theme.
- Add avatar images to `public/avatars/`.
- You can update the system prompt in `main.py` to change Kero's personality or instructions. By default, Kero is themed as a helpful frog assistant.

## License
MIT License
