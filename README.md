# Meme Economy Telegram Bot

Повноцінний Telegram-бот з мемною економікою, колекційними предметами та маркетплейсом. Проєкт побудовано на `aiogram 3`, використовує PostgreSQL + SQLAlchemy (async) і готовий до деплою на Render.

## Можливості
- валюта **VUSD**, стартові та щоденні бонуси
- реферальна програма з пасивним доходом 10% від бонусів друга
- 195 унікальних предметів із рідкостями, кольорами та типами (card/gif/artifact)
- 11 кейсів з pity-системою, ультра- і колекторськими випусками
- маркетплейс з комісією 5%, миттєвий викуп ботом, лідерборди
- щоденне нарахування Collector Points скриптом `scheduler/cron_daily.py`

## Структура
```
.
├─ app/
│  ├─ main.py                # запуск long polling
│  ├─ config.py              # Pydantic Settings (.env)
│  ├─ db/                    # база, моделі, Alembic
│  ├─ services/              # бізнес-логіка (users, cases, market, pricing...)
│  ├─ handlers/              # aiogram-роутери команд
│  ├─ seeds/                 # catalog.json, cases.json, seed.py
│  ├─ scheduler/cron_daily.py# щоденні CP
│  └─ texts/keyboards/utils  # повідомлення, клавіатури, утиліти
├─ requirements.txt
├─ alembic.ini + app/db/migrations
├─ render.yaml, Procfile, runtime.txt
├─ tests/                    # pytest з асинхронними тестами
└─ README.md
```

## Локальний запуск
1. **Створіть віртуальне середовище** і встановіть залежності:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Створіть файл `.env`** на основі [.env.sample](.env.sample) і вкажіть `BOT_TOKEN`, `DATABASE_URL` (формат `postgresql+asyncpg://...`).
3. **Прогоніть міграції**:
   ```bash
   alembic upgrade head
   ```
4. **Засійте базу** предметами та кейсами:
   ```bash
   python app/seeds/seed.py
   ```
5. **Запустіть бота**:
   ```bash
   python -m app.main
   ```

## Рендер (Render.com)
1. Запуште репозиторій на GitHub.
2. На Render створіть *Blueprint* із файлу `render.yaml`.
3. Дочекайтесь створення БД та воркера. У сервісі встановіть змінні середовища `BOT_TOKEN` і `DATABASE_URL` (URL береться з вкладки бази даних).
4. Після деплою бот запуститься у режимі long polling, вебхуки не потрібні.

## Тести та якість коду
- юніт-тести: `pytest`
- лінтер (за бажанням): можна додати `ruff` або `flake8`
- логування важливих подій (`info` рівень) присутнє у сервісах та scheduler

## Безпека
- **Не комітьте реальні токени** Telegram або паролі БД. Використовуйте `.env`.
- На продакшені рекомендовано ввімкнути регулярний запуск `scheduler/cron_daily.py` (наприклад, Render Cron job).

Успішної торгівлі мемами! 🚀
