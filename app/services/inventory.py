"""Робота з інвентарем користувача."""

from __future__ import annotations

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import ItemRarity, UserItem


async def fetch_inventory(session: AsyncSession, user_id: int) -> list[UserItem]:
    """Повертає всі предмети користувача з підвантаженими Item."""

    result = await session.execute(
        select(UserItem).options(selectinload(UserItem.item)).where(UserItem.user_id == user_id)
    )
    return result.scalars().all()


async def toggle_cp_lock(session: AsyncSession, user_item: UserItem, locked: bool) -> None:
    """Встановлює прапорець, чи враховується предмет у CP."""

    user_item.locked_for_cp = locked
    await session.flush()


def daily_cp_gain(items: Sequence[UserItem]) -> int:
    """Рахує, скільки CP користувач отримає за добу."""

    rarity_weights: dict[ItemRarity, int] = {
        ItemRarity.COMMON: 1,
        ItemRarity.UNCOMMON: 2,
        ItemRarity.RARE: 5,
        ItemRarity.EPIC: 12,
        ItemRarity.LEGENDARY: 60,
        ItemRarity.UNIQUE: 180,
        ItemRarity.MYTHICAL: 600,
    }
    total = 0
    for owned in items:
        if owned.locked_for_cp:
            total += rarity_weights.get(owned.item.rarity, 0)
    return total
