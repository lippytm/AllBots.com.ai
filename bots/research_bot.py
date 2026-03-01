"""
ResearchBot — an AI-enhanced bot that automates information gathering tasks.
"""
from __future__ import annotations

from typing import Any

from .base_bot import BaseBot


class ResearchBot(BaseBot):
    """
    Template bot for AI-assisted research automation.

    In a production deployment this class would integrate with a search API,
    a document store, or an LLM.  Here it provides the structural scaffold
    that downstream implementations extend.
    """

    def __init__(self, name: str = "ResearchBot", sources: list[str] | None = None) -> None:
        super().__init__(name)
        self.sources: list[str] = sources or []

    def add_source(self, source: str) -> None:
        """Register a data source URI for the bot to query."""
        self.sources.append(source)
        self.logger.debug("Added source: %s", source)

    def run(self, task: Any) -> dict[str, Any]:
        """
        Execute a research task.

        Parameters
        ----------
        task:
            A plain-text query string or a structured dict with a ``query`` key.

        Returns
        -------
        dict with ``query``, ``sources_queried``, and a placeholder ``results`` list.
        """
        query = task if isinstance(task, str) else task.get("query", str(task))
        self.logger.info("Running research task: %r across %d sources", query, len(self.sources))
        return {
            "query": query,
            "sources_queried": list(self.sources),
            "results": [],  # Populated by a real search integration at runtime.
        }
