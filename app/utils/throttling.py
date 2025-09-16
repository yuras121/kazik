"""Примітивний антиспам для команд."""

from __future__ import annotations

import time
from typing import Callable, MutableMapping


class ThrottleManager:
    """Веде часові мітки викликів користувачів."""

    def __init__(self, ttl_seconds: int = 2) -> None:
        self.ttl_seconds = ttl_seconds
        self._storage: MutableMapping[int, float] = {}

    def check(self, user_id: int) -> bool:
        """Повертає True, якщо користувач не перевищив обмеження."""

        now = time.monotonic()
        last = self._storage.get(user_id)
        if last and now - last < self.ttl_seconds:
            return False
        self._storage[user_id] = now
        return True

    def wrap(self, handler: Callable[..., Callable]):  # type: ignore[type-arg]
        """Декоратор для обробників."""

        def decorator(func):  # type: ignore[no-untyped-def]
            async def inner(event):  # type: ignore[no-untyped-def]
                user_id = getattr(event.from_user, "id", None)
                if user_id is None or self.check(user_id):
                    return await func(event)
                return None

            return inner

        return decorator
