"""
bots
====
High-level template bots for AI-enhanced tasks.

Each template is designed to be composed with the adaptive_engine and
advanced_swarms modules, providing a production-ready starting point for
common real-world automation scenarios.
"""

from .base_bot import BaseBot
from .research_bot import ResearchBot

__all__ = ["BaseBot", "ResearchBot"]
