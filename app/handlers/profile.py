"""Команда /profile."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import inventory as inventory_service, users
from app.texts.ua import PROFILE_TEMPLATE

router = Router()

RANKS: list[tuple[int, str]] = [
    (0, "Bronze"),
    (500, "Silver"),
    (2_000, "Gold"),
    (5_000, "Platinum"),
    (10_000, "Diamond"),
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
    text = PROFILE_TEMPLATE.format(
        username=message.from_user.full_name,
        vusd=user.vusd,
        cp=user.cp,
        rank=rank,
        mythic=user.mythic_count,
    )
    text += f"\nПредметів у колекції: <b>{len(items)}</b>"
    await message.answer(text)
