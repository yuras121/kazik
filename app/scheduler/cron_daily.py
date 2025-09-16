"""Щоденний перерахунок Collector Points."""

from __future__ import annotations

import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.base import get_session
from app.db.models import User, UserItem
from app.services.inventory import daily_cp_gain

logger = logging.getLogger(__name__)


async def process() -> None:
    """Нараховує CP усім користувачам за предмети в інвентарі."""

    async with get_session() as session:
        result = await session.execute(
            select(User).options(selectinload(User.inventory).selectinload(UserItem.item))
        )
        users = result.scalars().all()
        for user in users:
            gain = daily_cp_gain(user.inventory)
            if gain:
                user.cp += gain
                logger.info("Нараховано %s CP користувачу %s", gain, user.id)
        await session.commit()


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(process())


if __name__ == "__main__":
    main()
