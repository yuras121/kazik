"""Команда /balance."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import users
from app.texts.ua import BALANCE_TEMPLATE

router = Router()


@router.message(Command("balance"))
async def cmd_balance(message: Message) -> None:
    """Показує баланс користувача."""

    if message.from_user is None:
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session,
            tg_id=message.from_user.id,
            username=message.from_user.username,
        )
        await session.commit()

    await message.answer(BALANCE_TEMPLATE.format(vusd=user.vusd, cp=user.cp))
