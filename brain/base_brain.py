"""Base brain module — abstract foundation for all AI Brain kit modules."""

from __future__ import annotations

import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Any

import openai

logger = logging.getLogger(__name__)


class BaseBrain(ABC):
    """Abstract base class for every AI Brain module.

    Subclasses implement :meth:`think` to provide domain-specific
    intelligence.  Retry logic, OpenAI client initialisation, and
    structured logging are all handled here so individual modules can
    stay focused on their reasoning task.
    """

    #: Maximum number of OpenAI call retries before raising.
    MAX_RETRIES: int = 3
    #: Seconds to wait between retries (exponential back-off multiplier).
    RETRY_DELAY: float = 1.0

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
    ) -> None:
        self.model = model
        self._client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Human-readable name of this brain module."""
        return self.__class__.__name__

    def process(self, context: dict[str, Any]) -> dict[str, Any]:
        """Entry point called by the kit orchestrator.

        Validates *context*, delegates to :meth:`think`, and wraps the
        result in a standardised envelope.
        """
        self.logger.info("Brain %s processing context", self.name)
        result = self._call_with_retry(context)
        return {"brain": self.name, "status": "ok", "result": result}

    # ------------------------------------------------------------------
    # Abstract interface for subclasses
    # ------------------------------------------------------------------

    @abstractmethod
    def think(self, context: dict[str, Any]) -> Any:
        """Perform the domain-specific reasoning step.

        Args:
            context: Arbitrary key/value pairs describing the current
                     situation (e.g. conversation history, repo state).

        Returns:
            Any JSON-serialisable value representing the brain's output.
        """

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _call_with_retry(self, context: dict[str, Any]) -> Any:
        """Call :meth:`think` with exponential back-off on transient errors."""
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                return self.think(context)
            except openai.RateLimitError as exc:
                if attempt == self.MAX_RETRIES:
                    raise
                wait = self.RETRY_DELAY * (2 ** (attempt - 1))
                self.logger.warning(
                    "Rate limit hit (%s), retrying in %.1fs …", exc, wait
                )
                time.sleep(wait)
            except openai.APIError as exc:
                if attempt == self.MAX_RETRIES:
                    raise
                wait = self.RETRY_DELAY * (2 ** (attempt - 1))
                self.logger.warning("API error (%s), retrying in %.1fs …", exc, wait)
                time.sleep(wait)
        return None  # unreachable, but satisfies type checkers

    def _chat(self, system: str, user: str, **kwargs: Any) -> str:
        """Convenience wrapper around the OpenAI Chat Completions API."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            **kwargs,
        )
        return response.choices[0].message.content or ""
