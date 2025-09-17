"""Команда /help."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.keyboards.common import main_menu_keyboard
from app.texts.ua import HELP_TEXT

router = Router()


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Відправляє список команд."""

    await message.answer(HELP_TEXT, reply_markup=main_menu_keyboard())
