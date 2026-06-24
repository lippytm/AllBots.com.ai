"""
tests/test_adaptive_engine.py
Tests for the adaptive_engine package.
"""
import pytest

from adaptive_engine.profile_manager import ProfileManager
from adaptive_engine.adapter import IntelligenceAdapter


class TestProfileManager:
    def test_load_new_profile_returns_defaults(self, tmp_path):
        pm = ProfileManager(storage_dir=str(tmp_path))
        profile = pm.load("user_001")
        assert profile["user_id"] == "user_001"
        assert profile["preferences"] == {}
        assert profile["history"] == []

    def test_save_and_reload(self, tmp_path):
        pm = ProfileManager(storage_dir=str(tmp_path))
        pm.save("user_002", {"user_id": "user_002", "preferences": {"lang": "en"}, "history": []})
        profile = pm.load("user_002")
        assert profile["preferences"]["lang"] == "en"

    def test_update_persists_key(self, tmp_path):
        pm = ProfileManager(storage_dir=str(tmp_path))
        pm.update("user_003", "theme", "dark")
        profile = pm.load("user_003")
        assert profile["preferences"]["theme"] == "dark"


class TestIntelligenceAdapter:
    def test_adapt_returns_response_and_metadata(self, tmp_path):
        pm = ProfileManager(storage_dir=str(tmp_path))
        adapter = IntelligenceAdapter(profile_manager=pm)
        result = adapter.adapt("user_001", "hello")
        assert result["response"] == "hello"
        assert result["adapted_for"] == "user_001"
        assert "preferences_applied" in result

    def test_record_interaction_appends_to_history(self, tmp_path):
        pm = ProfileManager(storage_dir=str(tmp_path))
        adapter = IntelligenceAdapter(profile_manager=pm)
        adapter.record_interaction("user_001", {"action": "search", "query": "AI"})
        profile = pm.load("user_001")
        assert len(profile["history"]) == 1
        assert profile["history"][0]["action"] == "search"
