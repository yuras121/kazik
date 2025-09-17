"""Команда /leaderboard."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import leaderboard as leaderboard_service
from app.texts.ua import LEADERBOARD_HEADER, LEADERBOARD_SECTION

router = Router()


def _format_entries(title: str, users_list, value_getter) -> str:
    lines = []
    for idx, user in enumerate(users_list, start=1):
        if user.username:
            name = f"@{html.escape(user.username)}"
        else:
            name = f"ID {user.id}"
        value = value_getter(user)
        lines.append(f"{idx}. {name} — {value}")
    body = "\n".join(lines) if lines else "Немає даних"
    return LEADERBOARD_SECTION.format(title=title, body=body)


@router.message(Command("leaderboard"))
@router.message(F.text == "🏆 Рейтинги")
async def cmd_leaderboard(message: Message) -> None:
    """Відображає три рейтинги."""

    async with get_session() as session:
        rich = await leaderboard_service.top_by_vusdt(session)
        collectors = await leaderboard_service.top_by_cp(session)
        mythic = await leaderboard_service.top_by_mythics(session)
        await session.commit()

    sections = [
        _format_entries("Баланс VUSDT", rich, lambda u: f"{u.vusdt} VUSDT"),
        _format_entries("Collector Points", collectors, lambda u: f"{u.cp} CP"),
        _format_entries("Міфіки", mythic, lambda u: f"{u.mythic_count}"),
    ]

    text = LEADERBOARD_HEADER + "\n\n" + "\n\n".join(sections)
    await message.answer(text)
