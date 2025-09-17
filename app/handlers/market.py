"""Команди маркетплейсу."""

from __future__ import annotations

import html

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.base import get_session
from app.db.models import ItemRarity, ItemType, UserItem
from app.keyboards.common import market_filters_keyboard
from app.services import market as market_service, users
from app.texts.ua import MARKET_EMPTY, MARKET_LISTING_CREATED
from app.utils.formatting import format_item_card

router = Router()

PAGE_SIZE = 5

FILTERS: dict[str, dict[str, object]] = {
    "sticker": {"item_types": {ItemType.STICKER}, "label": "🎨 Стікери"},
    "gif": {"item_types": {ItemType.GIF}, "label": "🎞️ Гіфи"},
    "legendary": {"rarities": {ItemRarity.LEGENDARY, ItemRarity.UNIQUE}, "label": "⭐ Легендарні"},
    "mythical": {"rarities": {ItemRarity.MYTHICAL}, "label": "🔥 Міфічні"},
}


async def _render_market(
    message: Message,
    *,
    page: int = 1,
    filter_key: str | None = None,
) -> None:
    """Рендерить список лотів з урахуванням фільтрів."""

    params = FILTERS.get(filter_key or "", {})
    item_types = params.get("item_types") if isinstance(params.get("item_types"), set) else None
    rarities = params.get("rarities") if isinstance(params.get("rarities"), set) else None
    label = params.get("label") if isinstance(params.get("label"), str) else None

    offset = (page - 1) * PAGE_SIZE

    async with get_session() as session:
        listings = await market_service.load_active_listings(
            session,
            limit=PAGE_SIZE,
            offset=offset,
            item_types=item_types,
            rarities=rarities,
        )
        await session.commit()

    if not listings:
        await message.answer(MARKET_EMPTY, reply_markup=market_filters_keyboard())
        return

    header = f"🛒 <b>Маркетплейс</b> • сторінка {page}"
    if label:
        header += f" • {label}"
    lines = [header]
    for listing in listings:
        card = format_item_card(listing.user_item.item, serial=listing.user_item.serial_no)
        seller_username = listing.seller.username if listing.seller else None
        seller_display = (
            f"@{html.escape(seller_username)}" if seller_username else f"ID {listing.seller_id}"
        )
        lines.append(
            f"Лот #{listing.id} за {listing.price} VUSDT\n"
            f"Продавець: {seller_display}\n"
            f"{card}"
        )

    lines.append("Купити: /buy_item <ID>")
    await message.answer("\n\n".join(lines), reply_markup=market_filters_keyboard())


@router.message(Command("market"))
@router.message(F.text == "🛒 Маркет")
async def cmd_market(message: Message) -> None:
    """Відображає активні лоти."""

    if message.from_user is None:
        return

    page = 1
    if message.text:
        parts = message.text.split(maxsplit=1)
        if len(parts) == 2 and parts[1].isdigit():
            page = max(1, int(parts[1]))

    filter_key = None
    if message.text:
        parts = message.text.split()
        if len(parts) >= 2:
            if parts[1].isdigit():
                page = max(1, int(parts[1]))
                if len(parts) >= 3:
                    filter_key = parts[2].lower()
            else:
                filter_key = parts[1].lower()
                if len(parts) >= 3 and parts[2].isdigit():
                    page = max(1, int(parts[2]))
    await _render_market(message, page=page, filter_key=filter_key)


@router.callback_query(F.data.startswith("market_filter:"))
async def cb_market_filter(callback: CallbackQuery) -> None:
    """Обробляє вибір фільтра в інлайн-кнопках."""

    filter_key = callback.data.split(":", maxsplit=1)[1]
    await callback.answer()
    if callback.message:
        await _render_market(callback.message, page=1, filter_key=filter_key)


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
