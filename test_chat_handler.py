"""
Unit tests for the chatbot handler module.

Tests intent detection, translation parsing, and mode switching logic.
"""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from chatbot.chat_handler import (
    INTENT_CASUAL,
    INTENT_CLEAR,
    INTENT_KB,
    INTENT_SWITCH_MODE,
    INTENT_TRANSLATE,
    detect_intent,
    detect_target_mode,
    extract_translation_parts,
    translate,
)


class TestDetectIntent:

    @pytest.mark.parametrize("text,expected", [
        ("how do you say hello in japanese", INTENT_TRANSLATE),
        ("translate hello to japanese", INTENT_TRANSLATE),
        ("what's dog in japanese", INTENT_TRANSLATE),
        ("what is the most spoken language", INTENT_KB),
        ("how many people speak japanese", INTENT_KB),
        ("tell me about japanese", INTENT_KB),
        ("clear", INTENT_CLEAR),
        ("clear history", INTENT_CLEAR),
        ("forget", INTENT_CLEAR),
        ("switch to translate mode", INTENT_SWITCH_MODE),
        ("translation mode", INTENT_SWITCH_MODE),
    ])
    def test_intent_detection(self, text, expected):
        assert detect_intent(text) == expected

    def test_translate_mode_overrides(self):
        assert detect_intent("hello", current_mode="translate") == INTENT_TRANSLATE

    def test_casual_fallback(self):
        assert detect_intent("hello there friend") == INTENT_CASUAL


class TestDetectTargetMode:

    @pytest.mark.parametrize("text,expected", [
        ("switch to translate", "translate"),
        ("switch to chat", "chat"),
        ("translation mode", "translate"),
        ("chat mode", "chat"),
    ])
    def test_mode_detection(self, text, expected):
        assert detect_target_mode(text) == expected


class TestExtractTranslationParts:

    def test_extracts_phrase(self):
        phrase, lang = extract_translation_parts("say hello in japanese")
        assert phrase != ""
        assert lang == "japanese"

    def test_extracts_simple_phrase(self):
        phrase, lang = extract_translation_parts("translate thank you to japanese")
        assert "thank" in phrase.lower()
        assert lang == "japanese"

    def test_empty_phrase_returns_empty(self):
        phrase, _ = extract_translation_parts("translate to japanese")
        assert phrase == ""


class TestTranslate:

    @pytest.fixture
    def mock_translator(self):
        with patch("chatbot.chat_handler.translator") as mock:
            mock.translate.return_value = "こんにちは"
            yield mock

    def test_returns_required_fields(self):
        result = translate("say hello in japanese")
        assert all(k in result for k in ["english_reply", "translated_word", "pronunciation", "language"])

    def test_includes_pronunciation(self):
        result = translate("say hello in japanese")
        assert result["pronunciation"] != ""

    def test_empty_phrase_prompts_user(self):
        result = translate("translate to japanese")
        assert "what word or phrase" in result["english_reply"].lower()
        assert result["translated_word"] == ""


class TestEdgeCases:

    def test_empty_string(self):
        assert detect_intent("") == INTENT_CASUAL

    def test_whitespace_only(self):
        assert detect_intent("   ") == INTENT_CASUAL

    def test_case_insensitive(self):
        assert detect_intent("clear") == INTENT_CLEAR
        assert detect_intent("CLEAR") == INTENT_CLEAR
        assert detect_intent("Clear") == INTENT_CLEAR
