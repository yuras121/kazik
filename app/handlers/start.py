"""Обробник команди /start."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from app.db.base import get_session
from app.services import users
from app.texts.ua import HELP_TEXT, WELCOME_TEXT

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject) -> None:
    """Створює користувача та видає стартовий бонус."""

    if message.from_user is None:
        return

    referral_code = command.args if command else None
    async with get_session() as session:
        user, created = await users.ensure_user(
            session,
            tg_id=message.from_user.id,
            username=message.from_user.username,
            referral_code=referral_code,
        )
        await session.commit()

    response = WELCOME_TEXT if created else "Радий бачити знову!"
    await message.answer(response)
    await message.answer(HELP_TEXT)
