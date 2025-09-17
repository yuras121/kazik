"""Заглушка для квестів."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.texts.ua import QUESTS_PLACEHOLDER

router = Router()


@router.message(Command("quests"))
@router.message(F.text == "🎯 Квести")
async def cmd_quests(message: Message) -> None:
    """Поки що надсилає повідомлення-заглушку."""

    await message.answer(QUESTS_PLACEHOLDER)
