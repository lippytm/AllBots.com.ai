"""Full-Stack Kit — complete AI Brain kit with all four brain modules.

Orchestrates :class:`~brain.LanguageBrain`, :class:`~brain.MemoryBrain`,
:class:`~brain.DecisionBrain`, and :class:`~brain.LearningBrain` for
maximum intelligence and self-improvement capability.
"""

from __future__ import annotations

import logging
from typing import Any

from brain import DecisionBrain, LanguageBrain, LearningBrain, MemoryBrain

logger = logging.getLogger(__name__)


class FullStackKit:
    """Full-stack brain kit: language + memory + decision + learning.

    Every interaction is automatically logged so the LearningBrain can
    surface insights and drive continuous improvement.

    Parameters
    ----------
    model:
        OpenAI model to use (default: ``"gpt-4o"``).
    api_key:
        OpenAI API key.  Falls back to the ``OPENAI_API_KEY`` env var.
    learning_log:
        Path to the JSONL file used by the LearningBrain.
    memory_store:
        Path to the JSON file used by the MemoryBrain.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
        learning_log: str = "learning_log.jsonl",
        memory_store: str = "memory_store.json",
    ) -> None:
        self.language = LanguageBrain(model=model, api_key=api_key)
        self.memory = MemoryBrain(model=model, api_key=api_key, store_path=memory_store)
        self.decision = DecisionBrain(model=model, api_key=api_key)
        self.learning = LearningBrain(model=model, api_key=api_key, log_path=learning_log)
        logger.info("FullStackKit initialised (model=%s)", model)

    # ------------------------------------------------------------------

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        """Process a context dict and return a fully-enriched response.

        Expected context keys
        ---------------------
        ``message``
            User message / event description.
        ``options``
            Optional candidate actions for the DecisionBrain.
        ``goal``
            Optional goal string (used when *options* are provided).
        ``feedback``
            Optional feedback signal (``"positive"`` / ``"negative"`` /
            free text) for the LearningBrain to record.
        """
        message: str = context.get("message", "")
        options: list[Any] = context.get("options", [])
        goal: str = context.get("goal", "")
        feedback: str | None = context.get("feedback")

        history = self.memory.think({"action": "get_history", "window": 10})

        sentiment = self.language.think({"task": "sentiment", "text": message})
        intent = self.language.think({"task": "classify", "text": message})

        if options and goal:
            facts = {
                "intent": intent.get("intent", ""),
                "sentiment": sentiment.get("sentiment", ""),
                "message": message,
            }
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

        self.learning.think({
            "action": "record",
            "interaction": {
                "input": message,
                "output": reply,
                "intent": intent,
                "sentiment": sentiment,
                "feedback": feedback or "",
            },
        })

        return {
            "kit": "full_stack",
            "reply": reply,
            "intent": intent,
            "sentiment": sentiment,
            "decision": decision_result,
            "chosen_action": chosen,
        }

    # ------------------------------------------------------------------

    def get_insights(self, limit: int = 50) -> dict[str, Any]:
        """Return learning insights from recent interactions."""
        return self.learning.think({"action": "analyse", "limit": limit})

    def get_recommendations(self, limit: int = 50) -> dict[str, Any]:
        """Return improvement recommendations from recent interactions."""
        return self.learning.think({"action": "recommend", "limit": limit})

    def remember(self, key: str, value: Any) -> dict[str, Any]:
        """Store a persistent fact in long-term memory."""
        return self.memory.think({"action": "remember", "key": key, "value": value})

    def recall(self, key: str) -> Any:
        """Retrieve a persistent fact from long-term memory."""
        return self.memory.think({"action": "recall", "key": key})
