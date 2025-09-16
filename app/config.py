"""Налаштування застосунку на базі Pydantic Settings."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Глобальні налаштування бота."""

    bot_token: str = Field(..., alias="BOT_TOKEN", description="Токен Telegram-бота")
    database_url: str = Field(..., alias="DATABASE_URL", description="Рядок підключення до PostgreSQL")

    start_bonus: int = Field(50, description="Сума VUSD за перший старт")
    daily_bonus: int = Field(20, description="Щоденний бонус VUSD")
    referral_bonus: int = Field(50, description="Винагорода за запрошення друга")
    referral_daily_percent: float = Field(0.10, description="% від щоденних бонусів реферала")
    referral_daily_days: int = Field(7, description="Тривалість нарахувань від щоденного бонусу реферала")

    pity_epic_threshold: int = Field(10, description="Кількість відкриттів без Epic+ до посилення ваги")
    pity_epic_step: float = Field(1.2, description="Множник збільшення ваги Epic при кожному кроці")
    pity_legendary_step: float = Field(1.3, description="Множник збільшення ваги Legendary")
    pity_mythic_step: float = Field(1.5, description="Множник збільшення ваги Mythic")

    collector_case_cp_requirement: int = Field(5_000, description="Поріг CP для Collector Case")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", case_sensitive=False)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Повертає кешовані налаштування."""

    return Settings()
