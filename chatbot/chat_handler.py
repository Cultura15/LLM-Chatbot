import re

import jaconv
from deep_translator import GoogleTranslator

from knowledge_base.kb_loader import search as search_kb
from llm.engine import ask, clear_history


translator = GoogleTranslator(source='en', target='ja')

# Intent types
INTENT_TRANSLATE = "translate"
INTENT_KB = "knowledge"
INTENT_CASUAL = "casual"
INTENT_CLEAR = "clear"
INTENT_SWITCH_MODE = "switch_mode"

# Only match explicit translation requests
TRANSLATE_PATTERNS = [
    r"how do you say",
    r"how to say",
    r"say .* in ",
    r"translate .* to ",
    r"translate .* in ",
    r"what is .* in ",
    r"what's .* in ",
    r"what does .* mean in ",
]

KB_PATTERNS = [
    r"what (is|are|s|the)",
    r"how many",
    r"which (language|country)",
    r"most spoken",
    r"language.*facts",
    r"interesting.*language",
    r"tell me about",
    r"explain",
]

SWITCH_PATTERNS = [
    r"switch.*mode",
    r"change.*mode",
    r"go to.*mode",
    r"(translation|translate) mode",
    r"(chat|conversation) mode",
    r"^(let'?s\s+)?translate\s+to\s+(japanese|japanese?)",
    r"^(let'?s\s+)?translate$",
]

# Supported languages for extraction
LANGUAGES = ["japanese"]


def detect_intent(text: str, current_mode: str = "chat") -> str:
    text_lower = text.lower().strip()

    if any(re.search(p, text_lower) for p in SWITCH_PATTERNS):
        return INTENT_SWITCH_MODE

    if text_lower in ("clear", "clear history", "forget", "start over"):
        return INTENT_CLEAR

    if current_mode == "translate":
        return INTENT_TRANSLATE

    # Check KB before translation to avoid misclassifying factual questions
    for pattern in KB_PATTERNS:
        if re.search(pattern, text_lower):
            return INTENT_KB

    for pattern in TRANSLATE_PATTERNS:
        if re.search(pattern, text_lower):
            return INTENT_TRANSLATE

    return INTENT_CASUAL


def detect_target_mode(text: str) -> str:
    text_lower = text.lower()
    if "translate" in text_lower or "translation" in text_lower:
        return "translate"
    if "chat" in text_lower or "conversation" in text_lower:
        return "chat"
    return "chat"


def extract_translation_parts(text: str) -> tuple[str, str]:
    text_lower = text.lower().strip()
    target_lang = "japanese"
    text_modified = text_lower

    # Normalize "japan" to "japanese" if needed
    if "japan" in text_lower and "japanese" not in text_lower:
        text_modified = text_modified.replace("japan", "japanese")

    for lang in LANGUAGES:
        if f"in {lang}" in text_modified or f"to {lang}" in text_modified:
            target_lang = lang
            break

    # Strip common prefixes and language references to isolate the phrase
    phrase = text_modified
    for prefix in ["how do you say", "how to say", "translate", "what is", "what's"]:
        phrase = re.sub(rf'\b{re.escape(prefix)}\b', '', phrase)

    for lang in LANGUAGES:
        phrase = phrase.replace(f" in {lang}", "")
        phrase = phrase.replace(f" to {lang}", "")

    phrase = phrase.strip(" ?.,!")
    phrase = re.sub(r'\s+', ' ', phrase).strip()

    return phrase, target_lang


def translate(text: str) -> dict:
    phrase, target_lang = extract_translation_parts(text)

    if not phrase or len(phrase) < 2:
        return {
            "english_reply": "Sure! What word or phrase would you like me to translate to Japanese?",
            "translated_word": "",
            "pronunciation": "",
            "language": target_lang,
        }

    try:
        translated_word = translator.translate(phrase)

        # Convert to romaji via hiragana
        hiragana = jaconv.kata2hira(translated_word)
        pronunciation = jaconv.kana2alphabet(hiragana)

        return {
            "english_reply": f"'{phrase}' in {target_lang} is: {translated_word}",
            "translated_word": translated_word,
            "pronunciation": pronunciation,
            "language": target_lang,
        }

    except Exception as e:
        return {
            "english_reply": f"Sorry, I couldn't translate that. Error: {str(e)}",
            "translated_word": "",
            "pronunciation": "",
            "language": target_lang,
        }


def handle_kb(text: str) -> str:
    context = search_kb(text)
    if not context:
        return ask(text, "").strip()
    return ask(text, context).strip()


def chat(text: str, current_mode: str = "chat") -> dict:
    intent = detect_intent(text, current_mode)

    if intent == INTENT_SWITCH_MODE:
        target_mode = detect_target_mode(text)
        return {
            "response": f"Switched to {target_mode} mode!",
            "mode_change": target_mode,
            "is_translation": False,
        }

    if intent == INTENT_CLEAR:
        clear_history()
        return {
            "response": "Got it! I've forgotten our conversation. What would you like to talk about?",
            "is_translation": False,
        }

    if intent == INTENT_TRANSLATE:
        result = translate(text)
        return {
            "response": result["english_reply"],
            "translated_word": result["translated_word"],
            "pronunciation": result["pronunciation"],
            "language": result["language"],
            "is_translation": True,
        }

    if intent == INTENT_KB:
        return {
            "response": handle_kb(text),
            "is_translation": False,
        }

    return {
        "response": ask(text, "").strip(),
        "is_translation": False,
    }