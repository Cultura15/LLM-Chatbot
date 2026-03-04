import os
import re

import httpx


OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "phi3.5:latest")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

SYSTEM_PROMPT = (
    "You are Lingua, a Japanese language helper.\n\n"
    "Reply in ENGLISH only.\n"
    "Keep answers SHORT — 1 to 2 sentences only.\n"
    "No lists, no bullet points, no notes.\n"
    "Stop after 2 sentences. Do not continue."
)

chat_history = []


def ask(prompt: str, use_context: str = "", system_override: str = "") -> str:
    global chat_history

    os.environ["OLLAMA_DEBUG"] = "0"
    os.environ["OLLAMA_LOG_LEVEL"] = "error"

    # Build message list with system prompt, optional context, and history
    active_system = system_override if system_override else SYSTEM_PROMPT
    messages = [{"role": "system", "content": active_system}]

    if use_context:
        messages.append({"role": "system", "content": f"Use this context:\n\n{use_context}"})

    messages.extend(chat_history[-10:])
    messages.append({"role": "user", "content": prompt})

    try:
        client = httpx.Client(timeout=120)
        response = client.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": MAX_TOKENS,
                    "temperature": TEMPERATURE,
                },
            },
        )
        client.close()

        if response.status_code != 200:
            raise Exception(f"Ollama returned {response.status_code}: {response.text}")

        assistant_msg = response.json()["message"]["content"].strip()

        # Truncate to 2 sentences max
        sentence_ends = [m.end() for m in re.finditer(r'[.!?](?:\s|$)', assistant_msg)]
        if len(sentence_ends) >= 2:
            assistant_msg = assistant_msg[:sentence_ends[1]].strip()
        elif len(sentence_ends) == 1:
            assistant_msg = assistant_msg[:sentence_ends[0]].strip()

        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": assistant_msg})

        return assistant_msg

    except httpx.ConnectError:
        raise Exception("Cannot connect to Ollama. Is Ollama running?")
    except Exception as e:
        raise Exception(f"Ollama error: {e}")


def clear_history():
    global chat_history
    chat_history = []