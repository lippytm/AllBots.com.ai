"""
adaptive_engine
===============
Modules for adapting bot intelligence dynamically.

This package exposes the primary entry points for building and updating
per-user, per-context intelligence profiles that drive personalized bot
behavior across the AllBots.com.ai platform.
"""

from .profile_manager import ProfileManager
from .adapter import IntelligenceAdapter

__all__ = ["ProfileManager", "IntelligenceAdapter"]
