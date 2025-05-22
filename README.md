# Kero: Chainlit + Ollama Chatbot

Kero is a local chatbot web app built with [Chainlit](https://www.chainlit.io/) and [Ollama](https://ollama.com/), featuring image upload and contextual conversation memory. It uses the `gemma3:4b` model by default and runs entirely on your machine.

## Features
- Conversational AI with context memory
- Image upload and vision support
- Customizable theme (see `public/theme.json`)
- Local, private, and fast

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) installed and available in your PATH
- (Optional) Virtual environment for Python dependencies

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
4. Make sure Ollama is installed and the `gemma3:4b` model is available:
   ```bash
   ollama pull gemma3:4b
   ```

## Usage
Run the chatbot with:
```bash
python run_chat.py
```
This will start the Ollama server (if not already running) and launch the Chainlit app.

The web UI will be available at [http://localhost:8000](http://localhost:8000) by default.

## File Overview
- `main.py` — Chainlit app logic (chat, image upload, context)
- `run_chat.py` — Script to launch Ollama and Chainlit together
- `requirements.txt` — Python dependencies
- `public/` — Theme and avatar assets

## Customization
- Edit `public/theme.json` to change the UI theme.
- Add avatar images to `public/avatars/`.

## License
MIT License
