import re

import speech_recognition as sr


recognizer = sr.Recognizer()
recognizer.pause_threshold = 2.0
recognizer.non_speaking_duration = 1.5

print("Calibrating microphone...")
with sr.Microphone() as _source:
    recognizer.adjust_for_ambient_noise(_source, duration=1.0)
print("Microphone ready.")


def normalize_punctuation(text: str) -> str:
    if not text:
        return text

    text = text.strip()
    text = text[0].upper() + text[1:] if text else text

    if not text[-1] in '.!?':
        text += '.'

    text = re.sub(r'\bi\b', 'I', text)

    return text


def listen() -> str:
    with sr.Microphone() as source:
        print("Listening... (speak now, pause when done)")

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        text = normalize_punctuation(text)
        print(f"You (voice): {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand what you said.")
        return ""
    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return ""