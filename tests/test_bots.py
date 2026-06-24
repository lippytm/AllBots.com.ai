"""
tests/test_bots.py
Tests for the bots package.
"""
import pytest

from bots.base_bot import BaseBot
from bots.research_bot import ResearchBot


class _ConcreteBot(BaseBot):
    """Minimal concrete implementation of BaseBot for testing."""

    def run(self, task):
        return f"done:{task}"


class TestBaseBot:
    def test_instantiation_and_repr(self):
        bot = _ConcreteBot(name="test_bot")
        assert bot.name == "test_bot"
        assert "test_bot" in repr(bot)

    def test_run_returns_value(self):
        bot = _ConcreteBot(name="runner")
        assert bot.run("ping") == "done:ping"

    def test_abstract_prevents_direct_instantiation(self):
        with pytest.raises(TypeError):
            BaseBot(name="abstract")  # type: ignore[abstract]


class TestResearchBot:
    def test_default_name(self):
        bot = ResearchBot()
        assert bot.name == "ResearchBot"

    def test_run_with_string_task(self):
        bot = ResearchBot(sources=["https://example.com"])
        result = bot.run("AI news")
        assert result["query"] == "AI news"
        assert result["sources_queried"] == ["https://example.com"]
        assert isinstance(result["results"], list)

    def test_run_with_dict_task(self):
        bot = ResearchBot()
        result = bot.run({"query": "swarm robotics"})
        assert result["query"] == "swarm robotics"

    def test_add_source(self):
        bot = ResearchBot()
        bot.add_source("https://arxiv.org")
        assert bot.sources == ["https://arxiv.org"]
