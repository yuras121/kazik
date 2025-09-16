"""Українські текстові шаблони для бота."""

WELCOME_TEXT = (
    "Вітаємо в <b>Meme Economy</b>!\n\n"
    "Тримай стартовий бонус <b>+50 VUSD</b> та починай будувати імперію мемів.\n"
    "Використовуй /cases, щоб відкрити свій перший кейс, або /daily для щоденного бонусу."
)

HELP_TEXT = (
    "Команди бота:\n"
    "/start – почати гру та отримати бонус\n"
    "/help – довідка\n"
    "/balance – показати баланс\n"
    "/daily – щоденний бонус\n"
    "/cases – перегляд кейсів\n"
    "/open_case <код> – відкрити кейс\n"
    "/inventory – твоя колекція\n"
    "/market – маркетплейс\n"
    "/sell_to_bot <ID> – миттєвий викуп\n"
    "/list_item <ID> <ціна> – виставити лот\n"
    "/buy_item <ID> – купити лот\n"
    "/leaderboard – рейтинги\n"
    "/refer – реферальна програма"
)

DAILY_ALREADY_CLAIMED = "Щоденний бонус уже отримано. Повертайся пізніше!"
DAILY_SUCCESS = "Щоденний бонус +20 VUSD зараховано. Мемна імперія росте!"

BALANCE_TEMPLATE = "На твоєму рахунку: <b>{vusd} VUSD</b>. Загальний CP: <b>{cp}</b>."

NO_CASE_FOUND = "Кейс із таким кодом не знайдено. Перевір список через /cases."
CASE_LOCKED_CP = "Цей кейс відкривається лише з достатнім рівнем Collector Points."

OPEN_CASE_NOT_ENOUGH = "Недостатньо VUSD для відкриття кейсу."
OPEN_CASE_SUCCESS = (
    "Відкриваємо кейс <b>{case_name}</b> за {price} VUSD...\n"
    "Тобі випав {item_card}!"
)

INVENTORY_EMPTY = "Твій інвентар поки що порожній. Відкрий кейс або купи предмет на маркеті!"

REFERRAL_MESSAGE = (
    "Запрошуй друзів та заробляй!\n"
    "Твоє посилання: <code>{link}</code>\n"
    "За кожного друга: +50 VUSD та 10% від його щоденних бонусів протягом 7 днів."
)

MARKET_EMPTY = "Наразі активних лотів немає. Повернись трохи згодом!"
MARKET_LISTING_CREATED = "Лот #{listing_id} створено. Успіхів у продажах!"
MARKET_PURCHASE_SUCCESS = "Покупку завершено! Предмет уже в твоєму інвентарі."
MARKET_SELL_SUCCESS = "Ура! Лот продано, VUSD зараховано."

PROFILE_TEMPLATE = (
    "<b>{username}</b>\n"
    "Баланс: <b>{vusd} VUSD</b>\n"
    "Collector Points: <b>{cp}</b>\n"
    "Ранг: <b>{rank}</b>\n"
    "Міфічних предметів: <b>{mythic}</b>"
)

LEADERBOARD_HEADER = "🏆 <b>Рейтинги Мемної Біржі</b>"
LEADERBOARD_SECTION = "{title}:\n{body}"
