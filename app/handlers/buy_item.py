"""Команда /buy_item."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.base import get_session
from app.db.models import MarketListing
from app.services import market as market_service, users
from app.texts.ua import MARKET_PURCHASE_SUCCESS

router = Router()


@router.message(Command("buy_item"))
async def cmd_buy_item(message: Message) -> None:
    """Купівля лоту."""

    if message.from_user is None or message.text is None:
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Формат: /buy_item <ID>")
        return

    try:
        listing_id = int(parts[1])
    except ValueError:
        await message.answer("ID має бути числом")
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        listing = await session.scalar(
            select(MarketListing)
            .where(MarketListing.id == listing_id)
            .options(
                selectinload(MarketListing.user_item).selectinload(MarketListing.user_item.item),
                selectinload(MarketListing.seller),
            )
        )
        if not listing:
            await message.answer("Лот не знайдено")
            return
        try:
            await market_service.buy_listing(session, user, listing)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await session.commit()

    await message.answer(MARKET_PURCHASE_SUCCESS)
