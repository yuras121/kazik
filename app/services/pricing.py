"""Розрахунки вартості предметів."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from app.db.models.item import Item, ItemColor, ItemRarity, ItemType

RARITY_BASE: dict[ItemRarity, int] = {
    ItemRarity.COMMON: 5,
    ItemRarity.UNCOMMON: 12,
    ItemRarity.RARE: 28,
    ItemRarity.EPIC: 90,
    ItemRarity.LEGENDARY: 220,
    ItemRarity.UNIQUE: 600,
    ItemRarity.MYTHICAL: 2_000,
}

TYPE_MULTIPLIER: dict[ItemType, float] = {
    ItemType.STICKER: 1.0,
    ItemType.GIF: 1.6,
    ItemType.ARTIFACT: 2.4,
    ItemType.AVATAR: 2.0,
    ItemType.FRAME: 1.8,
    ItemType.CARD: 1.0,
}

COLOR_MULTIPLIER: dict[ItemColor, float] = {
    ItemColor.STANDARD: 1.0,
    ItemColor.SILVER: 1.25,
    ItemColor.GOLD: 1.5,
    ItemColor.RAINBOW: 2.0,
}


def compute_base_price(rarity: ItemRarity, item_type: ItemType, color: ItemColor) -> int:
    """Обчислює базову ціну викупу з урахуванням рідкості, типу та кольору."""

    base = RARITY_BASE[rarity]
    multiplier = TYPE_MULTIPLIER[item_type] * COLOR_MULTIPLIER[color]
    value = Decimal(base * multiplier).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(value)


def calculate_buyout_price(item: Item) -> int:
    """Повертає вартість миттєвого викупу для предмета."""

    return compute_base_price(item.rarity, item.type, item.color)
