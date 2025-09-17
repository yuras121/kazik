"""Перегляд кейсів."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from sqlalchemy import select

from app.config import get_settings
from app.db.base import get_session
from app.db.models import Case
from app.services import users

router = Router()


@router.message(Command("cases"))
@router.message(F.text == "📦 Відкрити кейс")
async def cmd_cases(message: Message) -> None:
    """Відображає список кейсів."""

    if message.from_user is None:
        return

    settings = get_settings()

    async with get_session() as session:
        user, _ = await users.ensure_user(
            session, tg_id=message.from_user.id, username=message.from_user.username
        )
        cases = await session.scalars(select(Case).order_by(Case.price))
        cases_list = cases.all()
        await session.commit()

    lines = ["📦 <b>Кейси доступні до відкриття:</b>"]
    for case in cases_list:
        locked = case.cp_requirement and user.cp < case.cp_requirement
        status = "🔓" if not locked else "🔒"
        requirement = f" • CP ≥ {case.cp_requirement}" if case.cp_requirement else ""
        lines.append(f"{status} <b>{case.name}</b> ({case.code}) — {case.price} VUSDT{requirement}")
    if settings.collector_case_cp_requirement:
        lines.append(
            "🏆 Collector Case відкривається від "
            f"{settings.collector_case_cp_requirement} CP."
        )

    await message.answer("\n".join(lines))
