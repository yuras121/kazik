"""Реєстрація роутерів aiogram."""

from __future__ import annotations

from aiogram import Dispatcher

from app.handlers import (
    balance,
    buy_item,
    cases,
    daily,
    help,
    inventory,
    leaderboard,
    market,
    open_case,
    profile,
    refer,
    sell_to_bot,
    start,
)


def register_handlers(dp: Dispatcher) -> None:
    """Підключає всі модулі-обробники."""

    for module in (
        start,
        help,
        balance,
        daily,
        cases,
        open_case,
        inventory,
        profile,
        market,
        sell_to_bot,
        buy_item,
        leaderboard,
        refer,
    ):
        dp.include_router(module.router)
