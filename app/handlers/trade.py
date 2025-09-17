"""Команди трейдів."""

from __future__ import annotations

import html
import logging
from typing import Optional

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.db.models import TradeOffer, TradeStatus
from app.services import users
from app.texts.ua import TRADE_RECORDED, TRADE_USAGE

router = Router()


def _parse_trade_command(payload: str) -> Optional[tuple[str, str, str]]:
    parts = payload.split()
    if len(parts) < 3:
        return None
    target = parts[0].lstrip("@")
    if "for" not in parts:
        return None
    idx = parts.index("for")
    offer = " ".join(parts[1:idx])
    request = " ".join(parts[idx + 1 :])
    if not offer or not request:
        return None
    return target, offer, request


@router.message(Command("trade"))
@router.message(F.text == "🔄 Трейд")
async def cmd_trade(message: Message) -> None:
    """Створює запис трейду або показує інструкцію."""

    if message.from_user is None or message.text is None:
        return

    command, *rest = message.text.split(maxsplit=1)
    if not rest:
        await message.answer(TRADE_USAGE)
        return

    parsed = _parse_trade_command(rest[0])
    if parsed is None:
        await message.answer(TRADE_USAGE)
        return

    target_username, offer_item, request_item = parsed

    async with get_session() as session:
        creator, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        offer = TradeOffer(
            creator_id=creator.id,
            target_username=target_username,
            offer_item=offer_item,
            request_item=request_item,
            status=TradeStatus.OPEN,
        )
        session.add(offer)
        await session.commit()

    await message.answer(
        TRADE_RECORDED
        + "\n"
        + f"👤 Кому: @{html.escape(target_username)}\n"
        + f"🎁 Пропонуєш: {html.escape(offer_item)}\n"
        + f"✨ Хочеш: {html.escape(request_item)}"
    )

    target_user = None
    async with get_session() as session:
        target_user = await users.get_by_username(session, target_username)

    if target_user:
        try:
            await message.bot.send_message(
                target_user.tg_id,
                (
                    "🔔 Тобі прилетів трейд-запит!\n"
                    f"Від: {html.escape(message.from_user.full_name)}\n"
                    f"Пропозиція: {html.escape(offer_item)}\n"
                    f"У відповідь: {html.escape(request_item)}\n"
                    "Використай /trade @{sender} {their_item} for {your_item}, щоб відповісти."
                ).format(
                    sender=html.escape(message.from_user.username or message.from_user.full_name),
                    their_item=html.escape(request_item),
                    your_item=html.escape(offer_item),
                ),
            )
        except Exception:  # noqa: BLE001 - приватність бота
            logging.getLogger(__name__).info("Не вдалося повідомити адресата трейду")
