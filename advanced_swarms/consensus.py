"""
ConsensusProtocol — simple majority-vote consensus for swarm decision-making.
"""
from __future__ import annotations

import logging
from collections import Counter
from typing import Any, Callable, Iterable

logger = logging.getLogger(__name__)


class ConsensusProtocol:
    """
    Reaches agreement among a group of agents via majority vote.

    Each agent is a callable that accepts a *question* and returns a hashable
    answer.  The protocol collects all votes and returns the majority answer
    together with the full vote tally.
    """

    def __init__(self, agents: Iterable[Callable[[Any], Any]] | None = None) -> None:
        self.agents: list[Callable[[Any], Any]] = list(agents or [])

    def add_agent(self, agent: Callable[[Any], Any]) -> None:
        """Register an additional voting agent."""
        self.agents.append(agent)

    def vote(self, question: Any) -> dict[str, Any]:
        """
        Ask all agents to vote on *question* and return the consensus result.

        Returns
        -------
        dict with keys:
            - ``winner``: the majority answer (or ``None`` if no agents)
            - ``tally``: full vote counts
        """
        if not self.agents:
            logger.warning("No agents registered; returning empty consensus.")
            return {"winner": None, "tally": {}}

        votes = [agent(question) for agent in self.agents]
        tally = dict(Counter(votes))
        winner = max(tally, key=lambda k: tally[k])
        logger.info("Consensus reached: %s (tally=%s)", winner, tally)
        return {"winner": winner, "tally": tally}
