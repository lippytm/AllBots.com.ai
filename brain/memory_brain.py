"""Memory Brain — conversation state and long-term knowledge storage."""

from __future__ import annotations

import json
import os
from collections import deque
from typing import Any

from .base_brain import BaseBrain


class MemoryBrain(BaseBrain):
    """Manages short-term conversation context and persistent key-value memory.

    Short-term memory
    -----------------
    A fixed-size window of recent conversation turns kept in RAM.

    Long-term memory
    ----------------
    A lightweight JSON file on disk (``memory_store.json`` by default)
    for persisting facts across sessions.

    Context keys
    ------------
    ``action``
        One of ``"remember"``, ``"recall"``, ``"forget"``,
        ``"add_turn"``, ``"get_history"`` (default: ``"get_history"``).
    ``key``
        Lookup key for ``remember`` / ``recall`` / ``forget``.
    ``value``
        Value to store (used with ``remember``).
    ``turn``
        ``{"role": …, "content": …}`` dict to append (used with
        ``add_turn``).
    ``window``
        Number of recent turns to include in ``get_history`` (default:
        ``10``).
    """

    def __init__(
        self,
        *,
        short_term_limit: int = 20,
        store_path: str = "memory_store.json",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._short_term: deque[dict[str, str]] = deque(maxlen=short_term_limit)
        self._store_path = store_path
        self._long_term: dict[str, Any] = self._load_store()

    # ------------------------------------------------------------------

    def think(self, context: dict[str, Any]) -> Any:
        action = context.get("action", "get_history")

        if action == "remember":
            return self._remember(context["key"], context["value"])
        if action == "recall":
            return self._recall(context.get("key", ""))
        if action == "forget":
            return self._forget(context["key"])
        if action == "add_turn":
            return self._add_turn(context["turn"])
        if action == "get_history":
            return self._get_history(context.get("window", 10))
        if action == "summarise":
            return self._summarise_memory()
        return {"error": f"Unknown action: {action}"}

    # ------------------------------------------------------------------
    # Short-term memory
    # ------------------------------------------------------------------

    def _add_turn(self, turn: dict[str, str]) -> dict[str, Any]:
        self._short_term.append(turn)
        return {"added": turn, "short_term_size": len(self._short_term)}

    def _get_history(self, window: int) -> list[dict[str, str]]:
        turns = list(self._short_term)
        return turns[-window:] if window else turns

    # ------------------------------------------------------------------
    # Long-term memory
    # ------------------------------------------------------------------

    def _remember(self, key: str, value: Any) -> dict[str, Any]:
        self._long_term[key] = value
        self._save_store()
        return {"stored": {key: value}}

    def _recall(self, key: str) -> Any:
        if key:
            return self._long_term.get(key)
        return dict(self._long_term)

    def _forget(self, key: str) -> dict[str, Any]:
        removed = self._long_term.pop(key, None)
        self._save_store()
        return {"removed": key, "found": removed is not None}

    # ------------------------------------------------------------------
    # Synthesis
    # ------------------------------------------------------------------

    def _summarise_memory(self) -> str:
        history_text = json.dumps(self._get_history(10), indent=2)
        facts_text = json.dumps(self._long_term, indent=2)
        system = "You are the Memory Brain of an AllBots.com AI Bot."
        user = (
            "Summarise the following conversation history and stored facts "
            "into a concise paragraph that can be used to prime future "
            "responses.\n\n"
            f"History:\n{history_text}\n\nFacts:\n{facts_text}"
        )
        return self._chat(system, user)

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _load_store(self) -> dict[str, Any]:
        if os.path.exists(self._store_path):
            try:
                with open(self._store_path, encoding="utf-8") as fh:
                    return json.load(fh)
            except (json.JSONDecodeError, OSError):
                self.logger.warning("Could not load memory store; starting fresh.")
        return {}

    def _save_store(self) -> None:
        try:
            with open(self._store_path, "w", encoding="utf-8") as fh:
                json.dump(self._long_term, fh, indent=2)
        except OSError as exc:
            self.logger.error("Failed to save memory store: %s", exc)
