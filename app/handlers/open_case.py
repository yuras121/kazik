"""Відкриття кейсів."""

from __future__ import annotations

import asyncio
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import select

from app.db.base import get_session
from app.db.models import Case
from app.services import cases as case_service
from app.services import users
from app.texts.ua import (
    CASE_LOCKED_CP,
    NO_CASE_FOUND,
    OPEN_CASE_ANIMATION,
    OPEN_CASE_NOT_ENOUGH,
    OPEN_CASE_SUCCESS,
)
from app.utils.formatting import format_item_card

router = Router()


@router.message(Command("open_case"))
@router.message(Command("open"))
@router.message(F.text.startswith("/open "))
async def cmd_open_case(message: Message) -> None:
    """Відкриває кейс за кодом."""

    if message.from_user is None or message.text is None:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Вкажи код кейсу: /open PepeCase")
        return

    raw_code = parts[1].strip()
    if "_" in raw_code:
        case_code = raw_code.lower()
    else:
        case_code = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", raw_code).lower()
    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        case = await session.scalar(select(Case).where(Case.code == case_code))
        if not case:
            await message.answer(NO_CASE_FOUND)
            return
        if case.cp_requirement and user.cp < case.cp_requirement:
            await message.answer(CASE_LOCKED_CP)
            return
        if user.vusdt < case.price:
            await message.answer(OPEN_CASE_NOT_ENOUGH)
            return

        result = await case_service.open_case(session, user, case)
        await session.commit()

    item_card = format_item_card(result.item, serial=result.user_item.serial_no)
    for frame in OPEN_CASE_ANIMATION:
        await message.answer(frame)
        await asyncio.sleep(0.4)
    await message.answer(
        OPEN_CASE_SUCCESS.format(case_name=case.name, price=case.price, item_card=item_card)
    )
