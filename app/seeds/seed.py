"""Скрипт заповнення бази даних даними з JSON."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlalchemy import delete, select

from app.db.base import get_session
from app.db.models import Case, CaseItem, Item, ItemColor, ItemRarity, ItemType

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "catalog.json"
CASES_PATH = BASE_DIR / "cases.json"


async def seed_catalog() -> None:
    async with get_session() as session:
        with CATALOG_PATH.open(encoding="utf-8") as f:
            catalog = json.load(f)

        for entry in catalog:
            exists = await session.scalar(select(Item).where(Item.key == entry["key"]))
            if exists:
                continue
            item = Item(
                key=entry["key"],
                name=entry["name"],
                rarity=ItemRarity(entry["rarity"]),
                type=ItemType(entry["type"]),
                color=ItemColor(entry["color"]),
                cp_value=entry["cp_value"],
                base_buy_price=entry["base_buy_price"],
                image_url=entry.get("image_url"),
            )
            session.add(item)

        await session.commit()


async def seed_cases() -> None:
    async with get_session() as session:
        with CASES_PATH.open(encoding="utf-8") as f:
            cases = json.load(f)

        items_map = {
            item.key: item.id
            for item in (await session.execute(select(Item))).scalars().all()
        }

        for entry in cases:
            case = await session.scalar(select(Case).where(Case.code == entry["code"]))
            if not case:
                case = Case(
                    code=entry["code"],
                    name=entry["name"],
                    price=entry["price"],
                    pity_step=entry.get("pity_step", 1.0),
                    pity_threshold=entry.get("pity_threshold", 10),
                    cp_requirement=entry.get("cp_requirement"),
                    cover_image=entry.get("cover_image"),
                )
                session.add(case)
                await session.flush()
            else:
                case.name = entry["name"]
                case.price = entry["price"]
                case.pity_step = entry.get("pity_step", 1.0)
                case.pity_threshold = entry.get("pity_threshold", 10)
                case.cp_requirement = entry.get("cp_requirement")
                case.cover_image = entry.get("cover_image")
                await session.flush()

            await session.execute(delete(CaseItem).where(CaseItem.case_id == case.id))

            for item_entry in entry["items"]:
                item_id = items_map.get(item_entry["item_key"])
                if not item_id:
                    continue
                case_item = CaseItem(case_id=case.id, item_id=item_id, weight=item_entry["weight"])
                session.add(case_item)

        await session.commit()


async def main() -> None:
    await seed_catalog()
    await seed_cases()
    print("Seeder виконано успішно")


if __name__ == "__main__":
    asyncio.run(main())
