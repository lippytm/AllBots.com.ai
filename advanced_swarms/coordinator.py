"""
SwarmCoordinator — orchestrates a fleet of bots through task distribution.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Iterable

logger = logging.getLogger(__name__)


class SwarmCoordinator:
    """
    Distributes tasks across a registered pool of bot workers.

    Workers are plain callables that accept a single task payload and return
    a result.  The coordinator handles dispatch, basic load balancing, and
    result aggregation.
    """

    def __init__(self) -> None:
        self._workers: list[Callable[[Any], Any]] = []

    def register(self, worker: Callable[[Any], Any]) -> None:
        """Add a worker (bot callable) to the swarm."""
        self._workers.append(worker)
        logger.debug("Registered worker %s; pool size=%d", worker, len(self._workers))

    def dispatch(self, tasks: Iterable[Any]) -> list[Any]:
        """
        Assign each task to a worker in round-robin order.

        Returns a list of results in the same order as *tasks*.
        """
        if not self._workers:
            raise RuntimeError("No workers registered in the swarm.")

        results: list[Any] = []
        for idx, task in enumerate(tasks):
            worker = self._workers[idx % len(self._workers)]
            logger.info("Dispatching task %d to worker %s", idx, worker)
            results.append(worker(task))
        return results

    @property
    def size(self) -> int:
        """Number of workers currently in the swarm."""
        return len(self._workers)
