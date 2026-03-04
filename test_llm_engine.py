"""
Unit tests for the LLM engine module.

Tests the Ollama integration, message handling, and response processing.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_ollama(monkeypatch):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"message": {"content": "Test response"}}
    mock_client.post.return_value = mock_response
    mock_client.close = MagicMock()

    monkeypatch.setattr("llm.engine.httpx.Client", lambda *a, **kw: mock_client)
    return mock_client


class TestAskFunction:

    def test_makes_post_request(self, mock_ollama):
        from llm.engine import ask
        result = ask("Hello")
        mock_ollama.post.assert_called_once()
        assert "/api/chat" in mock_ollama.post.call_args[0][0]
        mock_ollama.close.assert_called_once()

    def test_includes_system_prompt(self, mock_ollama):
        from llm.engine import ask
        ask("test")
        call_json = mock_ollama.post.call_args[1]["json"]
        assert any(m["role"] == "system" for m in call_json["messages"])

    def test_includes_context_when_provided(self, mock_ollama):
        from llm.engine import ask
        ask("question", use_context="Some context")
        messages = mock_ollama.post.call_args[1]["json"]["messages"]
        assert any("Use this context" in m.get("content", "") for m in messages)

    def test_truncates_to_two_sentences(self, mock_ollama):
        mock_ollama.post.return_value.json.return_value = {
            "message": {"content": "First. Second. Third. Fourth!"}
        }
        from llm.engine import ask
        result = ask("test")
        assert "Third" not in result
        assert "Fourth" not in result

    def test_raises_on_connection_error(self, mock_ollama):
        import httpx
        mock_ollama.post.side_effect = httpx.ConnectError("Connection refused")
        from llm.engine import ask
        with pytest.raises(Exception) as exc:
            ask("test")
        assert "Cannot connect" in str(exc.value)

    def test_uses_configured_model(self, mock_ollama):
        from llm.engine import ask
        ask("test")
        call_json = mock_ollama.post.call_args[1]["json"]
        assert call_json["model"] == "phi3.5:latest"


class TestChatHistory:

    def test_history_accumulates(self, mock_ollama):
        import llm.engine
        llm.engine.chat_history = []
        from llm.engine import ask
        ask("Hello")
        ask("How are you?")
        assert len(llm.engine.chat_history) >= 4

    def test_clear_history_works(self, mock_ollama):
        import llm.engine
        llm.engine.chat_history = []
        from llm.engine import ask, clear_history
        ask("Hello")
        assert len(llm.engine.chat_history) > 0
        clear_history()
        assert len(llm.engine.chat_history) == 0


class TestSentenceTruncation:

    def test_truncates_multiple_sentences(self, mock_ollama):
        mock_ollama.post.return_value.json.return_value = {
            "message": {"content": "One. Two. Three. Four."}
        }
        from llm.engine import ask
        result = ask("test")
        assert result.count(".") <= 2

    def test_handles_single_sentence(self, mock_ollama):
        mock_ollama.post.return_value.json.return_value = {
            "message": {"content": "Just one sentence."}
        }
        from llm.engine import ask
        result = ask("test")
        assert "Just one sentence" in result


class TestConfiguration:

    def test_default_values_exist(self):
        from llm.engine import MAX_TOKENS, MODEL, OLLAMA_URL, TEMPERATURE
        assert OLLAMA_URL is not None
        assert MODEL is not None
        assert MAX_TOKENS is not None
        assert TEMPERATURE is not None
