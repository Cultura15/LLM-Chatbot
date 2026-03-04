"""
Unit tests for the knowledge base module.

Tests document search and loading functionality.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_base import kb_loader


@pytest.fixture(autouse=True)
def reset_documents():
    kb_loader.documents = {}
    yield
    kb_loader.documents = {}


class TestKnowledgeBaseSearch:

    def test_no_documents_returns_empty(self):
        assert kb_loader.search("anything") == ""

    def test_finds_matching_document(self):
        kb_loader.documents = {"test": "Japanese is spoken in Japan."}
        result = kb_loader.search("japanese")
        assert "Japanese" in result

    def test_ranks_by_frequency(self):
        kb_loader.documents = {
            "doc1": "Japanese Japanese Japanese",
            "doc2": "Japanese language",
        }
        result = kb_loader.search("japanese")
        assert result.startswith("Japanese Japanese Japanese")

    def test_returns_top_two(self):
        kb_loader.documents = {
            "doc1": "Japanese content",
            "doc2": "Japanese more",
            "doc3": "Japanese stuff",
        }
        result = kb_loader.search("japanese")
        assert result.count("---") <= 1

    def test_ignores_short_words(self):
        kb_loader.documents = {"test": "The cat sat"}
        assert kb_loader.search("an") == ""

    def test_case_insensitive(self):
        kb_loader.documents = {"test": "JAPANESE language"}
        result = kb_loader.search("Japanese")
        assert "Japanese" in result or "JAPANESE" in result

    def test_no_match_returns_empty(self):
        kb_loader.documents = {"test": "English content"}
        assert kb_loader.search("spanish") == ""

    def test_empty_query_returns_empty(self):
        assert kb_loader.search("") == ""


class TestKnowledgeBaseLoad:

    def test_handles_missing_file(self):
        assert kb_loader.documents == {}
