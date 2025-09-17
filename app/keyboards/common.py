"""Генерація клавіатур для бота."""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def cases_keyboard(cases: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """Клавіатура зі списком кейсів."""

    rows = [[InlineKeyboardButton(text=name, callback_data=f"case:{code}")] for code, name in cases]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def inventory_item_keyboard(user_item_id: int) -> InlineKeyboardMarkup:
    """Кнопки для швидких дій над предметом."""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤝 Продати боту", callback_data=f"sell:{user_item_id}")],
            [InlineKeyboardButton(text="📦 На маркет", callback_data=f"list:{user_item_id}")],
        ]
    )


def market_navigation_keyboard(page: int, has_next: bool) -> InlineKeyboardMarkup:
    """Посторінкова навігація маркету."""

    buttons: list[InlineKeyboardButton] = []
    if page > 1:
        buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"market:{page - 1}"))
    if has_next:
        buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"market:{page + 1}"))

    if not buttons:
        buttons.append(InlineKeyboardButton(text="Оновити", callback_data=f"market:{page}"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def market_filters_keyboard() -> InlineKeyboardMarkup:
    """Фільтри маркету за категоріями."""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Стікери", callback_data="market_filter:sticker"),
                InlineKeyboardButton(text="🎞️ Гіфи", callback_data="market_filter:gif"),
            ],
            [
                InlineKeyboardButton(text="⭐ Легендарні", callback_data="market_filter:legendary"),
                InlineKeyboardButton(text="🔥 Міфічні", callback_data="market_filter:mythical"),
            ],
        ]
    )


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Головна клавіатура з ключовими діями."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📦 Відкрити кейс"),
                KeyboardButton(text="🎁 Інвентар"),
            ],
            [
                KeyboardButton(text="💸 Продати боту"),
                KeyboardButton(text="🛒 Маркет"),
            ],
            [
                KeyboardButton(text="👤 Профіль"),
                KeyboardButton(text="🏆 Рейтинги"),
            ],
            [
                KeyboardButton(text="🔄 Трейд"),
                KeyboardButton(text="🎯 Квести"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Обери дію 👇",
    )
