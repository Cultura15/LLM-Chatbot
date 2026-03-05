# Lingua LLM Chatbot 

A voice-interactive chatbot for Japanese language learning and translation, powered by a locally-hosted LLM via Ollama. All inference runs on-device — no external API calls, no data sent to third-party services.

![Output Preview](https://raw.githubusercontent.com/Cultura15/LLM-Chatbot/main/assets/output.png)

![Output Preview 2](https://raw.githubusercontent.com/Cultura15/LLM-Chatbot/main/assets/output2.png)

## Overview

Built around an Ollama-backed inference engine (`phi3.5:latest`), the assistant supports two operational modes — **Translation** and **Conversational Chat** — both exposed through a voice I/O pipeline using `SpeechRecognition` + `pyttsx3`. A lightweight RAG layer performs keyword-matched retrieval against a local Markdown knowledge base to ground factual responses about Japanese language and culture.

## Core Features

- **Voice I/O Pipeline** — Real-time speech recognition via `SpeechRecognition` + `PyAudio`, with synthesized audio responses through `pyttsx3`. Microphone ambient noise calibration runs on startup.
- **Dual Interaction Modes** — Switchable at runtime between Translation Mode (English → Japanese with romanized pronunciation) and Chat Mode (open-domain Q&A on Japanese language and culture).
- **Local RAG Layer** — Factual queries are routed through a document retrieval step over a built-in knowledge base before being passed to the LLM, reducing hallucination on language-specific facts.
- **Fully Local Inference** — No cloud dependency. Model execution handled by Ollama (`phi3.5:latest`).

## Technical Stack

| Layer | Technology | Version |
|---|---|---|
| LLM Runtime | Ollama + `phi3.5` | `ollama >= 0.3.12`, model tag `phi3.5:latest` (3.8B, Q4_K_M) |
| Ollama HTTP API | REST `/api/chat` | Requires Ollama API schema `v0.3.x`+ (breaking changes from `v0.1.x`) |
| Voice Input | `SpeechRecognition` + `PyAudio` | `SpeechRecognition==3.10.4`, `PyAudio==0.2.14`, PortAudio `>= 19.7.0` |
| Voice Output | `pyttsx3` | `pyttsx3==2.90` (offline TTS, eSpeak-NG backend on Linux) |
| Intent Routing | Rule-based classifier | keyword-match + regex, no external NLP dependency |
| Knowledge Retrieval | Keyword search over local `.md` corpus | BM25-style token overlap |
| Runtime | Python | `3.10.x – 3.11.x` only — see constraint note below |
| Type Checking | Pyright | Configured via `pyrightconfig.json` — strict mode |
| Test Suite | `pytest` | `pytest==7.4.x` |

## Runtime Constraints

**Python `3.12+` is not supported.** The `PyAudio` C extension has an ABI incompatibility with CPython `3.12`'s updated stable ABI surface — it will build silently on some platforms but produce garbled or silent audio output at runtime. Pin to `3.10.x` or `3.11.x`.

**Isolation via `venv` is required, not optional.** System-level Python installs are not guaranteed to correctly resolve the `PyAudio` + `pyttsx3` + `SpeechRecognition` dependency graph, particularly on machines with multiple PortAudio versions present. Deviating from an isolated environment is the most common source of silent runtime failures reported on this stack.

**Ollama `v0.3.x` introduced a breaking schema change** to the `/api/chat` response envelope. If running `v0.1.x` or `v0.2.x`, message streaming and role parsing will silently fail. Verify your binary with `ollama --version` before running.

**Pyright strict mode is enforced** via `pyrightconfig.json`. If your editor or CI pipeline resolves types against a different Python environment than the active `venv`, you will see cascading type errors unrelated to the actual source. Point Pyright's `venvPath` to the project root and `venv` to the environment directory.

## Prerequisites

- **Ollama** `>= 0.3.12` — [ollama.com](https://ollama.com) — must be running (`ollama serve`) with `phi3.5` pulled via `ollama pull phi3.5`
- **Python** `3.10.x` or `3.11.x` — verify with `python --version` before creating your environment
- **PortAudio** `>= 19.7.0` — required at the system level by `PyAudio` (`brew install portaudio` / `apt-get install portaudio19-dev`)
- **eSpeak-NG** — required by `pyttsx3` on Linux (`apt-get install espeak-ng`)

## Runtime Commands

| Input | Action |
|---|---|
| `switch to translate mode` / `/translate` | Activate Translation Mode |
| `switch to chat mode` / `/chat` | Activate Chat Mode |
| `clear` | Flush conversation history |
| `exit` / `quit` / `bye` | Terminate session |
