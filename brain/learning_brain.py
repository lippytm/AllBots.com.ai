"""Learning Brain — adaptive learning from feedback and interaction data."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from .base_brain import BaseBrain


class LearningBrain(BaseBrain):
    """Collects feedback, identifies patterns, and adapts bot behaviour.

    The Learning Brain records interaction outcomes and uses GPT to
    surface actionable insights that can improve future responses or
    trigger retraining workflows.

    Context keys
    ------------
    ``action``
        One of ``"record"``, ``"analyse"``, ``"recommend"``
        (default: ``"analyse"``).
    ``interaction``
        Dict with ``input``, ``output``, and ``feedback`` keys — used
        with ``"record"``.
    ``limit``
        Maximum number of recent interactions to analyse (default: 50).
    """

    SYSTEM_PROMPT = (
        "You are the Learning Brain of an AllBots.com AI Bot. "
        "Identify patterns in interaction data and suggest concrete "
        "improvements. Return structured JSON."
    )

    def __init__(self, *, log_path: str = "learning_log.jsonl", **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._log_path = log_path

    # ------------------------------------------------------------------

    def think(self, context: dict[str, Any]) -> Any:
        action = context.get("action", "analyse")

        if action == "record":
            return self._record(context.get("interaction", {}))
        if action == "recommend":
            return self._recommend(context.get("limit", 50))
        return self._analyse(context.get("limit", 50))

    # ------------------------------------------------------------------

    def _record(self, interaction: dict[str, Any]) -> dict[str, Any]:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **interaction,
        }
        try:
            with open(self._log_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(entry) + "\n")
        except OSError as exc:
            self.logger.error("Could not write learning log: %s", exc)
        return {"recorded": entry}

    def _load_recent(self, limit: int) -> list[dict[str, Any]]:
        if not os.path.exists(self._log_path):
            return []
        entries: list[dict[str, Any]] = []
        try:
            with open(self._log_path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except OSError:
            pass
        return entries[-limit:]

    def _analyse(self, limit: int) -> dict[str, Any]:
        entries = self._load_recent(limit)
        if not entries:
            return {"insights": [], "total_interactions": 0}

        prompt = (
            "Analyse the following interaction log and return JSON with "
            "keys:\n"
            '- "insights": list of key patterns or findings\n'
            '- "positive_patterns": what is working well\n'
            '- "improvement_areas": where the bot struggles\n'
            '- "total_interactions": integer count\n\n'
            f"Log:\n{json.dumps(entries, indent=2)}"
        )
        raw = self._chat(
            self.SYSTEM_PROMPT, prompt, response_format={"type": "json_object"}
        )
        try:
            return json.loads(raw)
        except Exception:
            return {"raw": raw, "total_interactions": len(entries)}

    def _recommend(self, limit: int) -> dict[str, Any]:
        entries = self._load_recent(limit)
        if not entries:
            return {"recommendations": [], "total_interactions": 0}

        prompt = (
            "Based on the following interaction log, return JSON with "
            "key \"recommendations\" — a prioritised list of concrete "
            "actions (e.g. prompt adjustments, new rules, retraining "
            "triggers) to improve bot performance.\n\n"
            f"Log:\n{json.dumps(entries, indent=2)}"
        )
        raw = self._chat(
            self.SYSTEM_PROMPT, prompt, response_format={"type": "json_object"}
        )
        try:
            return json.loads(raw)
        except Exception:
            return {"raw": raw, "total_interactions": len(entries)}
