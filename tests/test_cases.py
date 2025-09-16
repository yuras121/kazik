"""Тести логіки кейсів."""

from __future__ import annotations

import pytest

from app.db.models import Case, CaseItem, Item, ItemColor, ItemRarity, ItemType, User
from app.services import cases as case_service


async def _create_basic_case(session, price: int = 100) -> tuple[Case, list[CaseItem], User]:
    items = [
        Item(key="common_card", name="Common", rarity=ItemRarity.COMMON, type=ItemType.CARD, color=ItemColor.STANDARD, cp_value=10, base_buy_price=1),
        Item(key="rare_card", name="Rare", rarity=ItemRarity.RARE, type=ItemType.CARD, color=ItemColor.STANDARD, cp_value=30, base_buy_price=5),
        Item(key="epic_card", name="Epic", rarity=ItemRarity.EPIC, type=ItemType.CARD, color=ItemColor.STANDARD, cp_value=120, base_buy_price=20),
        Item(key="legendary_card", name="Legendary", rarity=ItemRarity.LEGENDARY, type=ItemType.CARD, color=ItemColor.STANDARD, cp_value=600, base_buy_price=100),
    ]
    for item in items:
        session.add(item)
    await session.flush()

    case = Case(code="test", name="Test Case", price=price, pity_step=1.1, pity_threshold=5)
    session.add(case)
    await session.flush()

    case_items = [
        CaseItem(case_id=case.id, item_id=items[0].id, weight=10),
        CaseItem(case_id=case.id, item_id=items[1].id, weight=5),
        CaseItem(case_id=case.id, item_id=items[2].id, weight=2),
        CaseItem(case_id=case.id, item_id=items[3].id, weight=1),
    ]
    for ci in case_items:
        session.add(ci)
    await session.flush()

    user = User(tg_id=123, username="tester", ref_code="REFTEST", vusd=1_000, cp=0, mythic_count=0)
    session.add(user)
    await session.flush()

    return case, case_items, user


@pytest.mark.asyncio
async def test_pity_weights_scale_up(session, monkeypatch) -> None:
    case, case_items, user = await _create_basic_case(session)
    user.pity_counter = case.pity_threshold + 2

    captured: dict[str, list[float]] = {}

    def fake_weighted_choice(items, weights):  # type: ignore[no-untyped-def]
        captured["weights"] = list(weights)
        return items[0]

    monkeypatch.setattr("app.services.cases.rng.weighted_choice", fake_weighted_choice)

    await case_service.open_case(session, user, case)

    weights = captured["weights"]
    assert weights[2] > case_items[2].weight
    assert weights[3] > case_items[3].weight


@pytest.mark.asyncio
async def test_open_case_resets_pity_on_epic(session, monkeypatch) -> None:
    case, case_items, user = await _create_basic_case(session)
    user.pity_counter = case.pity_threshold + 1

    def pick_epic(items, weights):  # type: ignore[no-untyped-def]
        return items[2]

    monkeypatch.setattr("app.services.cases.rng.weighted_choice", pick_epic)

    result = await case_service.open_case(session, user, case)

    assert result.pity_reset is True
    assert user.pity_counter == 0
