"""
Unit tests for the voice/speech modules.

Tests speech input normalization - the only pure function worth testing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNormalizePunctuation:

    def test_adds_period_when_missing(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("hello world") == "Hello world."

    def test_preserves_period(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("hello world.") == "Hello world."

    def test_preserves_question_mark(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("how are you?") == "How are you?"

    def test_preserves_exclamation(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("great job!") == "Great job!"

    def test_capitalizes_first_letter(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("hello world").startswith("Hello")

    def test_lowercase_i_becomes_uppercase(self):
        from voice.speech_input import normalize_punctuation
        assert "I am here" in normalize_punctuation("i am here")

    def test_handles_empty_string(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("") == ""

    def test_strips_whitespace(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("  hello world  ") == "Hello world."

    def test_handles_proper_format(self):
        from voice.speech_input import normalize_punctuation
        assert normalize_punctuation("Hello! I am here.") == "Hello! I am here."
