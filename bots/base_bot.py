"""
BaseBot — abstract base class for all AllBots.com.ai template bots.
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class BaseBot(ABC):
    """
    Foundation class for every AI-enhanced bot in the AllBots.com.ai ecosystem.

    Subclasses must implement :meth:`run`, which accepts a task payload and
    returns a result.  The base class provides shared logging and a minimal
    lifecycle hook.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.logger = logging.getLogger(f"bots.{name}")

    @abstractmethod
    def run(self, task: Any) -> Any:
        """Execute the bot's primary task and return a result."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
