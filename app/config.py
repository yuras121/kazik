"""Налаштування застосунку на базі Pydantic Settings."""

from __future__ import annotations

from functools import lru_cache

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Глобальні налаштування бота."""

    bot_token: str = Field(..., alias="BOT_TOKEN", description="Токен Telegram-бота")
    database_url: str | None = Field(
        default=None,
        alias="DATABASE_URL",
        description="Рядок підключення до зовнішньої БД (PostgreSQL або інша)",
    )
    sqlite_path: str = Field(
        default="sqlite+aiosqlite:///./data/meme_economy.db",
        description="DSN для локальної SQLite, використовується за замовчуванням",
    )
    log_file: str = Field(
        default="logs/bot.log",
        description="Шлях до файлу з логами для дебагу",
    )

    start_bonus: int = Field(1_000, description="Сума VUSDT за перший старт")
    daily_bonus: int = Field(120, description="Щоденний бонус VUSDT")
    referral_bonus: int = Field(150, description="Винагорода за запрошення друга")
    referral_daily_percent: float = Field(0.10, description="% від щоденних бонусів реферала")
    referral_daily_days: int = Field(7, description="Тривалість нарахувань від щоденного бонусу реферала")

    pity_epic_threshold: int = Field(8, description="Кількість відкриттів без Epic+ до посилення ваги")
    pity_epic_step: float = Field(1.25, description="Множник збільшення ваги Epic при кожному кроці")
    pity_legendary_step: float = Field(1.35, description="Множник збільшення ваги Legendary")
    pity_unique_step: float = Field(1.45, description="Множник збільшення ваги Unique")
    pity_mythic_step: float = Field(1.7, description="Множник збільшення ваги Mythic")

    collector_case_cp_requirement: int = Field(15_000, description="Поріг CP для Collector Case")
    transfer_tax_rate: float = Field(0.05, description="Комісія на перекази між гравцями")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def database_dsn(self) -> str:
        """Повертає DSN БД з урахуванням дефолтного SQLite."""

        if self.database_url:
            return self.database_url
        # забезпечуємо існування директорії для SQLite
        sqlite_url = self.sqlite_path
        if sqlite_url.startswith("sqlite") and "///" in sqlite_url:
            path = sqlite_url.split("///", maxsplit=1)[1]
            if path:
                Path(path).expanduser().parent.mkdir(parents=True, exist_ok=True)
        return sqlite_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Повертає кешовані налаштування."""

    return Settings()
