"""Переказ VUSDT між гравцями."""

from __future__ import annotations

import html
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.db.base import get_session
from app.services import economy, users
from app.texts.ua import (
    TRANSFER_INVALID_AMOUNT,
    TRANSFER_NO_USER,
    TRANSFER_RECIPIENT,
    TRANSFER_SELF,
    TRANSFER_SUCCESS,
)

router = Router()


@router.message(Command("send"))
async def cmd_send(message: Message) -> None:
    """Обробляє команду /send."""

    if message.from_user is None or message.text is None:
        return

    parts = message.text.split()
    if len(parts) < 3:
        await message.answer("Формат: /send @користувач 100")
        return

    target_username = parts[1].lstrip("@")
    try:
        amount = int(parts[2])
    except ValueError:
        await message.answer(TRANSFER_INVALID_AMOUNT)
        return

    async with get_session() as session:
        sender, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        receiver = await users.get_by_username(session, target_username)
        if receiver is None:
            await message.answer(TRANSFER_NO_USER)
            return
        if receiver.id == sender.id:
            await message.answer(TRANSFER_SELF)
            return
        try:
            net, fee = await economy.transfer_between_users(session, sender, receiver, amount)
        except ValueError as exc:
            await message.answer(str(exc))
            return
        await session.commit()

    await message.answer(TRANSFER_SUCCESS.format(net=net, fee=fee))
    try:
        await message.bot.send_message(
            receiver.tg_id,
            TRANSFER_RECIPIENT.format(
                net=net,
                sender=html.escape(message.from_user.full_name),
            ),
        )
    except Exception:  # noqa: BLE001 - можемо не мати доступу до користувача
        logging.getLogger(__name__).warning("Не вдалося повідомити одержувача про переказ")
