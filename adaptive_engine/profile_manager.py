"""
ProfileManager — per-user intelligence profile storage and retrieval.
"""
from __future__ import annotations

import json
import os
from typing import Any


class ProfileManager:
    """Stores and retrieves per-user intelligence profiles on disk."""

    def __init__(self, storage_dir: str = ".profiles") -> None:
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _path(self, user_id: str) -> str:
        return os.path.join(self.storage_dir, f"{user_id}.json")

    def load(self, user_id: str) -> dict[str, Any]:
        """Load an existing profile, or return an empty profile."""
        path = self._path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        return {"user_id": user_id, "preferences": {}, "history": []}

    def save(self, user_id: str, profile: dict[str, Any]) -> None:
        """Persist a profile to disk."""
        with open(self._path(user_id), "w", encoding="utf-8") as fh:
            json.dump(profile, fh, indent=2)

    def update(self, user_id: str, key: str, value: Any) -> dict[str, Any]:
        """Update a single key in a profile and persist it."""
        profile = self.load(user_id)
        profile["preferences"][key] = value
        self.save(user_id, profile)
        return profile
