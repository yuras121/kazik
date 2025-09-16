"""Команди маркетплейсу."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.base import get_session
from app.db.models import UserItem
from app.services import market as market_service, users
from app.texts.ua import MARKET_EMPTY, MARKET_LISTING_CREATED
from app.utils.formatting import format_item_card

router = Router()

PAGE_SIZE = 5


@router.message(Command("market"))
async def cmd_market(message: Message) -> None:
    """Відображає активні лоти."""

    if message.from_user is None:
        return

    page = 1
    if message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 2 and parts[1].isdigit():
            page = max(1, int(parts[1]))

    offset = (page - 1) * PAGE_SIZE

    async with get_session() as session:
        listings = await market_service.load_active_listings(session, limit=PAGE_SIZE, offset=offset)
        await session.commit()

    if not listings:
        await message.answer(MARKET_EMPTY)
        return

    lines = [f"🛒 <b>Маркетплейс</b> • сторінка {page}"]
    for listing in listings:
        card = format_item_card(listing.user_item.item, serial=listing.user_item.serial_no)
        seller_username = listing.seller.username if listing.seller else None
        seller_display = f"@{seller_username}" if seller_username else f"ID {listing.seller_id}"
        lines.append(
            f"Лот #{listing.id} за {listing.price} VUSD\n"
            f"Продавець: {seller_display}\n"
            f"{card}"
        )

    lines.append("Купити: /buy_item <ID>")
    await message.answer("\n\n".join(lines))


@router.message(Command("list_item"))
async def cmd_list_item(message: Message) -> None:
    """Виставляє предмет на продаж."""

    if message.from_user is None or message.text is None:
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Формат: /list_item <ID> <ціна>")
        return

    try:
        user_item_id = int(parts[1])
        price = int(parts[2])
    except ValueError:
        await message.answer("ID та ціна мають бути числами")
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        user_item = await session.scalar(
            select(UserItem)
            .where(UserItem.id == user_item_id)
            .options(selectinload(UserItem.item), selectinload(UserItem.listing))
        )
        if not user_item:
            await message.answer("Предмет не знайдено")
            return
        try:
            listing = await market_service.list_item(session, user, user_item, price)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await session.commit()

    await message.answer(MARKET_LISTING_CREATED.format(listing_id=listing.id))
