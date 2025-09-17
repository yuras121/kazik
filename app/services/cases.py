"""Логіка відкриття кейсів."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import get_settings
from app.db.models import Case, CaseItem, Item, ItemRarity, TransactionKind, User, UserItem
from app.services import economy
from app.utils import rng


@dataclass(slots=True)
class CaseResult:
    """Результат відкриття кейсу."""

    user_item: UserItem
    item: Item
    pity_reset: bool


async def open_case(session: AsyncSession, user: User, case: Case) -> CaseResult:
    """Відкриває кейс, списуючи VUSD і повертаючи здобутий предмет."""

    await economy.withdraw(
        session, user, case.price, TransactionKind.CASE_PURCHASE, meta={"case": case.code}
    )

    case_items = await session.execute(
        select(CaseItem).options(selectinload(CaseItem.item)).where(CaseItem.case_id == case.id)
    )
    case_item_rows = case_items.scalars().all()
    if not case_item_rows:
        raise ValueError("Кейс не налаштований")

    settings = get_settings()
    pity_level = max(0, user.pity_counter - int(case.pity_threshold or settings.pity_epic_threshold) + 1)

    pool: list[tuple[CaseItem, float]] = []
    for entry in case_item_rows:
        weight = float(entry.weight)
        rarity = entry.item.rarity
        if pity_level > 0 and rarity in {
            ItemRarity.EPIC,
            ItemRarity.LEGENDARY,
            ItemRarity.UNIQUE,
            ItemRarity.MYTHICAL,
        }:
            if rarity is ItemRarity.EPIC:
                weight *= settings.pity_epic_step**pity_level
            elif rarity is ItemRarity.LEGENDARY:
                weight *= settings.pity_legendary_step**pity_level
            elif rarity is ItemRarity.UNIQUE:
                weight *= settings.pity_unique_step**pity_level
            else:
                weight *= settings.pity_mythic_step**pity_level
        pool.append((entry, weight))

    chosen_entry = rng.weighted_choice([p[0] for p in pool], [p[1] for p in pool])
    item = chosen_entry.item

    existing_serials = await session.scalars(select(UserItem.serial_no).where(UserItem.item_id == item.id))
    serial = rng.generate_serial(existing_serials.all())

    user_item = UserItem(user_id=user.id, item_id=item.id, serial_no=serial, locked_for_cp=True)
    session.add(user_item)
    await session.flush()

    pity_reset = item.rarity in {
        ItemRarity.EPIC,
        ItemRarity.LEGENDARY,
        ItemRarity.UNIQUE,
        ItemRarity.MYTHICAL,
    }
    if pity_reset:
        user.pity_counter = 0
    else:
        user.pity_counter += 1

    if item.rarity is ItemRarity.MYTHICAL:
        user.mythic_count += 1

    return CaseResult(user_item=user_item, item=item, pity_reset=pity_reset)
