"""Decision Brain — rule-based and AI-powered decision making."""

from __future__ import annotations

import json
from typing import Any

from .base_brain import BaseBrain


class DecisionBrain(BaseBrain):
    """Evaluates options and recommends actions.

    The Decision Brain combines deterministic rule evaluation with
    GPT-powered reasoning so bots can handle both structured workflows
    and open-ended situations.

    Context keys
    ------------
    ``goal``
        A natural-language description of what the bot is trying to
        achieve.
    ``options``
        A list of candidate actions / responses.
    ``constraints``
        Optional list of rules that must not be violated.
    ``facts``
        Optional dict of known facts relevant to the decision.
    ``mode``
        ``"rank"`` (rank all options) or ``"choose"`` (pick the single
        best option, default).
    """

    SYSTEM_PROMPT = (
        "You are the Decision Brain of an AllBots.com AI Bot. "
        "Evaluate options logically, respect all constraints, and "
        "return structured JSON."
    )

    def think(self, context: dict[str, Any]) -> Any:
        goal = context.get("goal", "")
        options = context.get("options", [])
        constraints = context.get("constraints", [])
        facts = context.get("facts", {})
        mode = context.get("mode", "choose")

        if not options:
            return {"error": "No options provided for decision making."}

        if mode == "rank":
            return self._rank_options(goal, options, constraints, facts)
        return self._choose_best(goal, options, constraints, facts)

    # ------------------------------------------------------------------

    def _choose_best(
        self,
        goal: str,
        options: list[Any],
        constraints: list[str],
        facts: dict[str, Any],
    ) -> dict[str, Any]:
        prompt = self._build_prompt(goal, options, constraints, facts, mode="choose")
        raw = self._chat(
            self.SYSTEM_PROMPT,
            prompt,
            response_format={"type": "json_object"},
        )
        try:
            result = json.loads(raw)
        except Exception:
            result = {"raw": raw}
        return result

    def _rank_options(
        self,
        goal: str,
        options: list[Any],
        constraints: list[str],
        facts: dict[str, Any],
    ) -> dict[str, Any]:
        prompt = self._build_prompt(goal, options, constraints, facts, mode="rank")
        raw = self._chat(
            self.SYSTEM_PROMPT,
            prompt,
            response_format={"type": "json_object"},
        )
        try:
            result = json.loads(raw)
        except Exception:
            result = {"raw": raw}
        return result

    # ------------------------------------------------------------------

    @staticmethod
    def _build_prompt(
        goal: str,
        options: list[Any],
        constraints: list[str],
        facts: dict[str, Any],
        mode: str,
    ) -> str:
        parts = [f"Goal: {goal}", f"Options: {json.dumps(options)}"]
        if constraints:
            parts.append(f"Constraints: {json.dumps(constraints)}")
        if facts:
            parts.append(f"Known facts: {json.dumps(facts)}")

        if mode == "choose":
            parts.append(
                'Return JSON with keys "choice" (the selected option) and '
                '"reasoning" (brief explanation).'
            )
        else:
            parts.append(
                'Return JSON with key "ranked" (list of options ordered best '
                'to worst) and "reasoning" (brief explanation for each).'
            )
        return "\n".join(parts)
