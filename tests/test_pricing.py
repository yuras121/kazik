"""Тести для цінової логіки."""

from __future__ import annotations

from app.db.models.item import Item, ItemColor, ItemRarity, ItemType
from app.services.pricing import calculate_buyout_price, compute_base_price


def test_compute_base_price_common_sticker() -> None:
    assert compute_base_price(ItemRarity.COMMON, ItemType.STICKER, ItemColor.STANDARD) == 5


def test_compute_base_price_gif_multiplier() -> None:
    assert compute_base_price(ItemRarity.RARE, ItemType.GIF, ItemColor.SILVER) == 56


def test_calculate_buyout_price_uses_item_fields() -> None:
    item = Item(
        key="test_item",
        name="Test",
        rarity=ItemRarity.LEGENDARY,
        type=ItemType.ARTIFACT,
        color=ItemColor.GOLD,
        cp_value=600,
        base_buy_price=0,
    )
    assert calculate_buyout_price(item) == 792
