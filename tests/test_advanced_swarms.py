"""
tests/test_advanced_swarms.py
Tests for the advanced_swarms package.
"""
import pytest

from advanced_swarms.coordinator import SwarmCoordinator
from advanced_swarms.consensus import ConsensusProtocol


class TestSwarmCoordinator:
    def test_dispatch_round_robin(self):
        coordinator = SwarmCoordinator()
        coordinator.register(lambda t: f"worker_a:{t}")
        coordinator.register(lambda t: f"worker_b:{t}")
        outputs = coordinator.dispatch(["task1", "task2", "task3"])
        assert outputs[0] == "worker_a:task1"
        assert outputs[1] == "worker_b:task2"
        assert outputs[2] == "worker_a:task3"

    def test_dispatch_no_workers_raises(self):
        coordinator = SwarmCoordinator()
        with pytest.raises(RuntimeError, match="No workers"):
            coordinator.dispatch(["task"])

    def test_size_reflects_registrations(self):
        coordinator = SwarmCoordinator()
        assert coordinator.size == 0
        coordinator.register(lambda t: t)
        assert coordinator.size == 1


class TestConsensusProtocol:
    def test_majority_vote(self):
        agents = [lambda q: "yes", lambda q: "yes", lambda q: "no"]
        cp = ConsensusProtocol(agents=agents)
        result = cp.vote("should we deploy?")
        assert result["winner"] == "yes"
        assert result["tally"]["yes"] == 2
        assert result["tally"]["no"] == 1

    def test_no_agents_returns_none(self):
        cp = ConsensusProtocol()
        result = cp.vote("anything")
        assert result["winner"] is None
        assert result["tally"] == {}

    def test_add_agent(self):
        cp = ConsensusProtocol()
        cp.add_agent(lambda q: "yes")
        result = cp.vote("test")
        assert result["winner"] == "yes"
