"""Форматування текстів для бота."""

from __future__ import annotations

from app.db.models.item import Item, ItemRarity, ItemType

RARITY_EMOJI: dict[ItemRarity, str] = {
    ItemRarity.COMMON: "🟢",
    ItemRarity.RARE: "🔵",
    ItemRarity.EPIC: "🟣",
    ItemRarity.LEGENDARY: "🟡",
    ItemRarity.MYTHIC: "🔥",
}

TYPE_LABELS: dict[ItemType, str] = {
    ItemType.CARD: "картка",
    ItemType.GIF: "гіф",
    ItemType.ARTIFACT: "артефакт",
}


def format_vusd(amount: int) -> str:
    """Форматує баланс VUSD."""

    return f"{amount:,} VUSD".replace(",", " ")


def format_item_card(item: Item, serial: str | None = None) -> str:
    """Повертає рядок з короткою інформацією про предмет."""

    rarity_badge = RARITY_EMOJI[item.rarity]
    serial_display = f"#{serial}" if serial else ""
    type_label = TYPE_LABELS[item.type]

    return (
        f"{rarity_badge} <b>{item.name}</b> {serial_display}\n"
        f"Тип: {type_label}\n"
        f"CP: <b>{item.cp_value}</b> • Викуп: <b>{item.base_buy_price} VUSD</b>"
    )
