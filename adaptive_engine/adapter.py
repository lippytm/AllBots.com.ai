"""
IntelligenceAdapter — applies a user profile to tune bot responses dynamically.
"""
from __future__ import annotations

from typing import Any

from .profile_manager import ProfileManager


class IntelligenceAdapter:
    """Wraps a bot callable and adjusts its behaviour based on user profile."""

    def __init__(self, profile_manager: ProfileManager | None = None) -> None:
        self.profile_manager = profile_manager or ProfileManager()

    def adapt(self, user_id: str, raw_response: Any) -> dict[str, Any]:
        """
        Enrich *raw_response* with context drawn from the user profile.

        Returns a dict with the original response plus adaptive metadata.
        """
        profile = self.profile_manager.load(user_id)
        return {
            "response": raw_response,
            "adapted_for": user_id,
            "preferences_applied": profile.get("preferences", {}),
        }

    def record_interaction(self, user_id: str, interaction: dict[str, Any]) -> None:
        """Append an interaction record to the user profile history."""
        profile = self.profile_manager.load(user_id)
        profile.setdefault("history", []).append(interaction)
        self.profile_manager.save(user_id, profile)
