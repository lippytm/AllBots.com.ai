"""
advanced_swarms
===============
Expandable swarm collaboration algorithms.

Provides multi-agent coordination primitives including consensus protocols,
task-auction mechanisms, and emergent-behaviour modeling for large-scale
AllBots.com.ai deployments.
"""

from .coordinator import SwarmCoordinator
from .consensus import ConsensusProtocol

__all__ = ["SwarmCoordinator", "ConsensusProtocol"]
