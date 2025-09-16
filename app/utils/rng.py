"""Корисні генератори та випадковість."""

from __future__ import annotations

import random
import secrets
import string
from typing import Iterable, Sequence, TypeVar

T = TypeVar("T")


def weighted_choice(items: Sequence[T], weights: Sequence[float]) -> T:
    """Повертає елемент згідно зі зваженим розподілом."""

    if not items or not weights:
        raise ValueError("Списки items та weights мають бути не порожні")
    if len(items) != len(weights):
        raise ValueError("Розмірність items та weights повинна збігатися")

    return random.choices(items, weights=weights, k=1)[0]


def generate_serial(existing: Iterable[str] | None = None) -> str:
    """Генерує серійний номер з ведучими нулями."""

    existing_set = set(existing or [])
    while True:
        number = random.randint(1, 99999)
        serial = f"{number:05d}"
        if serial not in existing_set:
            return serial


def generate_ref_code(length: int = 8) -> str:
    """Формує унікальний реферальний код."""

    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
