"""Команда /profile."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import inventory as inventory_service, users
from app.texts.ua import PROFILE_TEMPLATE
from app.utils.formatting import format_vusdt

router = Router()

RANKS: list[tuple[int, str]] = [
    (0, "Bronze"),
    (1_500, "Silver"),
    (5_000, "Gold"),
    (15_000, "Platinum"),
    (35_000, "Diamond"),
    (75_000, "Mythic"),
]


def resolve_rank(cp: int) -> str:
    """Повертає назву рангу за кількістю CP."""

    current = RANKS[0][1]
    for threshold, name in RANKS:
        if cp >= threshold:
            current = name
        else:
            break
    return current


@router.message(Command("profile"))
@router.message(F.text == "👤 Профіль")
async def cmd_profile(message: Message) -> None:
    """Показує розширений профіль."""

    if message.from_user is None:
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        items = await inventory_service.fetch_inventory(session, user.id)
        await session.commit()

    rank = resolve_rank(user.cp)
    daily_cp = inventory_service.daily_cp_gain(items)
    safe_name = html.escape(message.from_user.full_name)
    text = PROFILE_TEMPLATE.format(
        username=safe_name,
        vusdt=format_vusdt(user.vusdt),
        cp=user.cp,
        rank=rank,
        mythic=user.mythic_count,
        daily_cp=daily_cp,
    )
    text += f"\nПредметів у колекції: <b>{len(items)}</b>"
    await message.answer(text)
