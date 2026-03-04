import asyncio
import os
import tempfile

import edge_tts
import pygame


# Initialize pygame for audio playback
pygame.mixer.init()

VOICES = {
    # English
    "en": "en-US-AriaNeural",
    "english": "en-US-AriaNeural",

    # Japanese
    "ja": "ja-JP-NanamiNeural",
    "japanese": "ja-JP-NanamiNeural",
}

DEFAULT_VOICE = VOICES["en"]


async def speak_async(text: str, voice: str = DEFAULT_VOICE) -> None:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()

    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(temp_file.name)

        pygame.mixer.music.load(temp_file.name)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        try:
            os.unlink(temp_file.name)
        except Exception:
            pass


def speak(text: str) -> None:
    try:
        asyncio.run(speak_async(text, DEFAULT_VOICE))
    except Exception as e:
        print(f"Edge-tts failed: {e}")
        fallback_pyttsx3(text)


def speak_in_language(text: str, language: str) -> None:
    lang_lower = language.lower().strip()
    voice = VOICES.get(lang_lower)

    if not voice:
        for key, v in VOICES.items():
            if key in lang_lower or lang_lower in key:
                voice = v
                break

    if not voice:
        print(f"No native voice for '{language}', using English")
        voice = DEFAULT_VOICE

    try:
        asyncio.run(speak_async(text, voice))
    except Exception as e:
        print(f"Edge-tts failed: {e}")
        fallback_pyttsx3(text)


def fallback_pyttsx3(text: str) -> None:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"pyttsx3 also failed: {e}")