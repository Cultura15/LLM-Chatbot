# LLM Chatbot

A voice-powered chatbot that helps you learn Japanese through translation and conversation. Uses Ollama (local LLM) for AI responses.

## Features

- **Voice Input/Output** — Speak to the bot, hear responses
- **Translation Mode** — Translate English to Japanese with pronunciation
- **Chat Mode** — Ask questions about Japanese language and culture
- **Knowledge Base** — Answers factual questions from built-in documents
- **Local LLM** — Runs entirely on your machine via Ollama

#

![Project Image](https://raw.githubusercontent.com/Cultura15/LLM-Chatbot/main/assets/output.png)

#

![Project Image](https://raw.githubusercontent.com/Cultura15/LLM-Chatbot/main/assets/output2.png)

## Requirements

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note:** `PyAudio` may require installing PortAudio first:

| OS            | Command                                                                               |
| ------------- | ------------------------------------------------------------------------------------- |
| macOS         | `brew install portaudio`                                                              |
| Ubuntu/Debian | `sudo apt-get install portaudio19-dev`                                                |
| Windows       | Usually included, or install from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio |

### 2. Install Ollama

Download and install from https://ollama.com

Then pull the model:

```bash
ollama pull phi3.5
```

Start Ollama in the background:

```bash
ollama serve
```

### 3. (Optional) Configure Environment

Create a `.env` file in the project root (optional):

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=phi3.5:latest
MAX_TOKENS=150
TEMPERATURE=0.7
```

## Running the Chatbot

```bash
python cli.py
```

The bot will:

1. Calibrate your microphone
2. Greet you
3. Listen for your voice input
4. Respond via voice

### Commands

| Command                    | Action                         |
| -------------------------- | ------------------------------ |
| `switch to translate mode` | Enable translation mode        |
| `switch to chat mode`      | Enable chat mode               |
| `/translate`               | Quick switch to translate mode |
| `/chat`                    | Quick switch to chat mode      |
| `clear`                    | Reset conversation history     |
| `exit`, `quit`, `bye`      | Exit the bot                   |

## Running Tests

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

## Project Structure

```
llm-chatbot/
├── cli.py                 # Main entry point
├── chatbot/
│   └── chat_handler.py    # Intent detection, translation, chat logic
├── knowledge_base/
│   ├── kb_loader.py       # Document search
│   └── languages.md       # Built-in knowledge base
├── llm/
│   └── engine.py          # Ollama integration
├── voice/
│   ├── speech_input.py    # Voice recognition
│   └── speech_output.py   # Text-to-speech
└── test_*.py             # Unit tests
```

## Troubleshooting

**"Cannot connect to Ollama"**

- Make sure `ollama serve` is running
- Check the URL in `.env` matches your Ollama setup

**Microphone not working**

- Check system microphone permissions
- For PyAudio issues, see the PyAudio installation guide above

**No audio output**

- Check speakers/headphones
- Try pressing any key if audio is stuck
