"""Команда /daily."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import get_settings
from app.db.base import get_session
from app.services import economy, users
from app.texts.ua import DAILY_ALREADY_CLAIMED, DAILY_SUCCESS

router = Router()


@router.message(Command("daily"))
async def cmd_daily(message: Message) -> None:
    """Видає щоденний бонус."""

    if message.from_user is None:
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session,
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )
        success = await economy.grant_daily_bonus(session, user)
        await session.commit()

    if success:
        settings = get_settings()
        await message.answer(DAILY_SUCCESS.format(amount=settings.daily_bonus))
    else:
        await message.answer(DAILY_ALREADY_CLAIMED)
