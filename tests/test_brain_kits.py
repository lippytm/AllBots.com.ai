"""Unit tests for AI Brain Kits — no OpenAI calls required.

These tests validate the structure, configuration, and logic that does
not depend on live API access, so they can run in CI without secrets.
"""

from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
import types
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Ensure the repo root is on the path
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


# ---------------------------------------------------------------------------
# Helpers to stub out the openai package so tests work without the key
# ---------------------------------------------------------------------------

def _make_openai_stub() -> types.ModuleType:
    """Return a minimal stub that satisfies the brain module imports."""
    stub = types.ModuleType("openai")

    class _RateLimitError(Exception):
        pass

    class _APIError(Exception):
        pass

    stub.RateLimitError = _RateLimitError
    stub.APIError = _APIError
    stub.OpenAI = MagicMock()
    return stub


@pytest.fixture(autouse=True)
def patch_openai():
    """Patch openai globally for every test in this module."""
    stub = _make_openai_stub()
    with patch.dict("sys.modules", {"openai": stub}):
        # Reload brain modules so they pick up the stub
        for mod_name in list(sys.modules):
            if mod_name.startswith("brain") or mod_name.startswith("kits"):
                sys.modules.pop(mod_name, None)
        yield stub


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBrainImports:
    def test_brain_package_exports(self, patch_openai):
        from brain import (BaseBrain, DecisionBrain, LanguageBrain,
                           LearningBrain, MemoryBrain)

        assert issubclass(LanguageBrain, BaseBrain)
        assert issubclass(MemoryBrain, BaseBrain)
        assert issubclass(DecisionBrain, BaseBrain)
        assert issubclass(LearningBrain, BaseBrain)

    def test_kits_package_exports(self, patch_openai):
        from kits import FullStackKit, StandardKit, StarterKit

        for cls in (StarterKit, StandardKit, FullStackKit):
            assert callable(cls)


class TestMemoryBrain:
    def test_short_term_memory(self, patch_openai, tmp_path):
        from brain.memory_brain import MemoryBrain

        brain = MemoryBrain(store_path=str(tmp_path / "store.json"))
        brain.think({"action": "add_turn", "turn": {"role": "user", "content": "hello"}})
        history = brain.think({"action": "get_history", "window": 10})
        assert len(history) == 1
        assert history[0]["content"] == "hello"

    def test_long_term_memory(self, patch_openai, tmp_path):
        from brain.memory_brain import MemoryBrain

        store = str(tmp_path / "store.json")
        brain = MemoryBrain(store_path=store)
        brain.think({"action": "remember", "key": "user_name", "value": "Alice"})
        result = brain.think({"action": "recall", "key": "user_name"})
        assert result == "Alice"

        # Persists to disk
        with open(store) as fh:
            data = json.load(fh)
        assert data["user_name"] == "Alice"

    def test_forget(self, patch_openai, tmp_path):
        from brain.memory_brain import MemoryBrain

        brain = MemoryBrain(store_path=str(tmp_path / "store.json"))
        brain.think({"action": "remember", "key": "temp", "value": 42})
        brain.think({"action": "forget", "key": "temp"})
        assert brain.think({"action": "recall", "key": "temp"}) is None


class TestLearningBrain:
    def test_record_and_load(self, patch_openai, tmp_path):
        from brain.learning_brain import LearningBrain

        log = str(tmp_path / "log.jsonl")
        brain = LearningBrain(log_path=log)
        brain.think({
            "action": "record",
            "interaction": {"input": "hi", "output": "hello", "feedback": "positive"},
        })
        entries = brain._load_recent(10)
        assert len(entries) == 1
        assert entries[0]["input"] == "hi"

    def test_no_data_analyse(self, patch_openai, tmp_path):
        from brain.learning_brain import LearningBrain

        brain = LearningBrain(log_path=str(tmp_path / "empty.jsonl"))
        result = brain.think({"action": "analyse"})
        assert result["total_interactions"] == 0


class TestDecisionBrain:
    def test_no_options_error(self, patch_openai):
        from brain.decision_brain import DecisionBrain

        brain = DecisionBrain()
        result = brain.think({"goal": "test", "options": []})
        assert "error" in result


class TestDeployCLI:
    def test_deploy_to_single_target(self, patch_openai, capsys):
        """The deploy CLI should log the target repo and exit cleanly."""
        import deploy

        with patch.object(deploy, "deploy_to_repo") as mock_deploy:
            deploy.main.__globals__["sys"].argv = [
                "deploy.py", "--kit", "starter", "--target", "lippytm/AllBots.com.ai"
            ]
            # Call deploy logic directly (avoid SystemExit from argparse)
            import importlib
            import sys as _sys
            _sys.argv = ["deploy.py", "--kit", "starter", "--target", "lippytm/AllBots.com.ai"]
            deploy.main()
            mock_deploy.assert_called_once_with("starter", "lippytm/AllBots.com.ai")
