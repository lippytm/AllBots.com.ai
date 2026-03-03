"""Language Brain — natural-language understanding and generation."""

from __future__ import annotations

import json
from typing import Any

from .base_brain import BaseBrain


class LanguageBrain(BaseBrain):
    """Understands, summarises, and generates natural language.

    Capabilities
    ------------
    - Intent classification
    - Sentiment analysis
    - Text summarisation
    - Response generation

    Context keys (all optional)
    ---------------------------
    ``text``
        The raw text to analyse or respond to.
    ``task``
        One of ``"classify"``, ``"sentiment"``, ``"summarise"``,
        ``"generate"`` (default: ``"generate"``).
    ``history``
        List of ``{"role": …, "content": …}`` dicts representing prior
        conversation turns.
    """

    SYSTEM_PROMPT = (
        "You are the Language Brain of an AllBots.com AI Bot. "
        "Respond concisely and helpfully. "
        "Return structured JSON when asked to classify or analyse."
    )

    def think(self, context: dict[str, Any]) -> Any:
        text = context.get("text", "")
        task = context.get("task", "generate")
        history = context.get("history", [])

        if task == "classify":
            return self._classify_intent(text)
        if task == "sentiment":
            return self._analyse_sentiment(text)
        if task == "summarise":
            return self._summarise(text)
        return self._generate_response(text, history)

    # ------------------------------------------------------------------

    def _classify_intent(self, text: str) -> dict[str, Any]:
        prompt = (
            f'Classify the intent of the following message. '
            f'Return JSON with keys "intent" and "confidence" (0–1).\n\n'
            f'Message: """{text}"""'
        )
        raw = self._chat(self.SYSTEM_PROMPT, prompt, response_format={"type": "json_object"})
        try:
            return json.loads(raw)
        except Exception:
            return {"intent": "unknown", "confidence": 0.0, "raw": raw}

    def _analyse_sentiment(self, text: str) -> dict[str, Any]:
        prompt = (
            f'Analyse the sentiment of the following text. '
            f'Return JSON with keys "sentiment" (positive/neutral/negative) '
            f'and "score" (-1 to 1).\n\nText: """{text}"""'
        )
        raw = self._chat(self.SYSTEM_PROMPT, prompt, response_format={"type": "json_object"})
        try:
            return json.loads(raw)
        except Exception:
            return {"sentiment": "neutral", "score": 0.0, "raw": raw}

    def _summarise(self, text: str) -> str:
        prompt = f'Summarise the following text in 2–3 sentences:\n\n"""{text}"""'
        return self._chat(self.SYSTEM_PROMPT, prompt)

    def _generate_response(self, text: str, history: list[dict[str, str]]) -> str:
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": text})
        response = self._client.chat.completions.create(
            model=self.model, messages=messages
        )
        return response.choices[0].message.content or ""
