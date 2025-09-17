"""Форматування текстів для бота."""

from __future__ import annotations

from app.db.models.item import Item, ItemRarity, ItemType

RARITY_EMOJI: dict[ItemRarity, str] = {
    ItemRarity.COMMON: "🟢",
    ItemRarity.UNCOMMON: "🔹",
    ItemRarity.RARE: "🔵",
    ItemRarity.EPIC: "🟣",
    ItemRarity.LEGENDARY: "🟡",
    ItemRarity.UNIQUE: "💎",
    ItemRarity.MYTHICAL: "🔥",
}

TYPE_LABELS: dict[ItemType, str] = {
    ItemType.STICKER: "стікер",
    ItemType.GIF: "гіф",
    ItemType.ARTIFACT: "артефакт",
    ItemType.AVATAR: "аватар",
    ItemType.FRAME: "фрейм",
    ItemType.CARD: "картка",
}


def format_vusdt(amount: int) -> str:
    """Форматує баланс VUSDT."""

    return f"{amount:,} VUSDT".replace(",", " ")


def format_item_card(item: Item, serial: str | None = None) -> str:
    """Повертає рядок з короткою інформацією про предмет."""

    rarity_badge = RARITY_EMOJI[item.rarity]
    serial_display = f"#{serial}" if serial else ""
    type_label = TYPE_LABELS.get(item.type, item.type.value)

    return (
        f"{rarity_badge} <b>{item.name}</b> {serial_display}\n"
        f"Тип: {type_label}\n"
        f"CP: <b>{item.cp_value}</b> • Викуп: <b>{item.base_buy_price} VUSDT</b>"
    )
