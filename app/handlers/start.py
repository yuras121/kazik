"""Обробник команди /start."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message

from app.config import get_settings
from app.db.base import get_session
from app.keyboards.common import main_menu_keyboard
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

    settings = get_settings()
    response = (
        WELCOME_TEXT.format(start_bonus=settings.start_bonus)
        if created
        else "👋 З поверненням до Meme Economy!"
    )
    await message.answer(response, reply_markup=main_menu_keyboard())
    await message.answer(HELP_TEXT)
