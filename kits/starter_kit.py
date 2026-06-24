"""Starter Kit — minimal AI Brain kit for getting started quickly.

This kit wires up just the :class:`~brain.LanguageBrain` so a bot can
understand and respond to natural language with minimal configuration.
"""

from __future__ import annotations

import logging
from typing import Any

from brain import LanguageBrain, MemoryBrain

logger = logging.getLogger(__name__)


class StarterKit:
    """Minimal brain kit: language understanding + short-term memory.

    Parameters
    ----------
    model:
        OpenAI model to use (default: ``"gpt-4o-mini"`` for lower cost).
    api_key:
        OpenAI API key.  Falls back to the ``OPENAI_API_KEY`` env var.
    """

    def __init__(self, model: str = "gpt-4o-mini", api_key: str | None = None) -> None:
        self.language = LanguageBrain(model=model, api_key=api_key)
        self.memory = MemoryBrain(model=model, api_key=api_key)
        logger.info("StarterKit initialised (model=%s)", model)

    # ------------------------------------------------------------------

    def chat(self, user_message: str) -> str:
        """Process a user message and return the bot's reply.

        Conversation turns are automatically stored in short-term memory
        so context is preserved across calls.
        """
        history = self.memory.think({"action": "get_history", "window": 10})

        response = self.language.think(
            {"task": "generate", "text": user_message, "history": history}
        )

        self.memory.think(
            {"action": "add_turn", "turn": {"role": "user", "content": user_message}}
        )
        self.memory.think(
            {"action": "add_turn", "turn": {"role": "assistant", "content": response}}
        )

        return response

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Generic entry point compatible with the deploy workflow.

        Args:
            context: Must contain ``"message"`` key with user input.

        Returns:
            Dict with ``"reply"`` and ``"kit"`` keys.
        """
        message = context.get("message", "")
        reply = self.chat(message)
        return {"kit": "starter", "reply": reply}
