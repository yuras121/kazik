"""Команда /inventory."""

from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import inventory as inventory_service, users
from app.texts.ua import INVENTORY_EMPTY
from app.utils.formatting import format_item_card

router = Router()


@router.message(Command("inventory"))
async def cmd_inventory(message: Message) -> None:
    """Виводить предмети користувача."""

    if message.from_user is None:
        return

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        items = await inventory_service.fetch_inventory(session, user.id)
        await session.commit()

    if not items:
        await message.answer(INVENTORY_EMPTY)
        return

    lines = ["🧳 <b>Твій інвентар:</b>"]
    for owned in items:
        card = format_item_card(owned.item, serial=owned.serial_no)
        lines.append(f"ID {owned.id}: {card}")

    lines.append("\nКоманди: /sell_to_bot <ID>, /list_item <ID> <ціна>")
    await message.answer("\n\n".join(lines))
