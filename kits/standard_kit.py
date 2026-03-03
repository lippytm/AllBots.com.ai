"""Standard Kit — balanced AI Brain kit for everyday bot deployments.

Combines language understanding, memory, and decision-making in a
single easy-to-use orchestrator.
"""

from __future__ import annotations

import logging
from typing import Any

from brain import DecisionBrain, LanguageBrain, MemoryBrain

logger = logging.getLogger(__name__)


class StandardKit:
    """Standard brain kit: language + memory + decision making.

    Parameters
    ----------
    model:
        OpenAI model to use (default: ``"gpt-4o"``).
    api_key:
        OpenAI API key.  Falls back to the ``OPENAI_API_KEY`` env var.
    """

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None) -> None:
        self.language = LanguageBrain(model=model, api_key=api_key)
        self.memory = MemoryBrain(model=model, api_key=api_key)
        self.decision = DecisionBrain(model=model, api_key=api_key)
        logger.info("StandardKit initialised (model=%s)", model)

    # ------------------------------------------------------------------

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Process a context dict and return a structured response.

        Expected context keys
        ---------------------
        ``message``
            User message / event description.
        ``options``
            Optional list of candidate actions for the DecisionBrain.
        ``goal``
            Optional goal string used when *options* are provided.
        """
        message: str = context.get("message", "")
        options: list[Any] = context.get("options", [])
        goal: str = context.get("goal", "")

        history = self.memory.think({"action": "get_history", "window": 10})

        intent_result = self.language.think({"task": "classify", "text": message})

        if options and goal:
            facts = {"intent": intent_result.get("intent", ""), "message": message}
            decision_result = self.decision.think(
                {"goal": goal, "options": options, "facts": facts}
            )
            chosen = decision_result.get("choice", options[0])
        else:
            decision_result = {}
            chosen = None

        reply = self.language.think(
            {"task": "generate", "text": message, "history": history}
        )

        self.memory.think({"action": "add_turn", "turn": {"role": "user", "content": message}})
        self.memory.think({"action": "add_turn", "turn": {"role": "assistant", "content": reply}})

        return {
            "kit": "standard",
            "reply": reply,
            "intent": intent_result,
            "decision": decision_result,
            "chosen_action": chosen,
        }
