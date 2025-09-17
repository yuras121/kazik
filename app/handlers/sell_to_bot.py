"""Команда /sell_to_bot."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.base import get_session
from app.db.models import UserItem
from app.services import market as market_service, users

router = Router()


@router.message(Command("sell_to_bot"))
@router.message(F.text == "💸 Продати боту")
async def cmd_sell_to_bot(message: Message) -> None:
    """Миттєвий продаж предмета боту."""

    if message.from_user is None or message.text is None:
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Формат: /sell_to_bot <ID>")
        return

    try:
        user_item_id = int(parts[1])
    except ValueError:
        await message.answer("ID має бути числом")
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        user_item = await session.scalar(
            select(UserItem).where(UserItem.id == user_item_id).options(selectinload(UserItem.item))
        )
        if not user_item:
            await message.answer("Предмет не знайдено")
            return
        try:
            price = await market_service.sell_to_bot(session, user, user_item)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await session.commit()

    await message.answer(f"Предмет продано боту за {price} VUSDT. Баланс оновлено!")
