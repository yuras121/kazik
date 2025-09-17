"""Українські текстові шаблони для бота."""

WELCOME_TEXT = (
    "👋 Вітаємо в <b>Meme Economy 2.0</b>!\n"
    "Ти отримуєш стартовий капітал <b>{start_bonus} VUSDT</b> і можеш одразу відкривати кейси.\n"
    "Скористайся кнопками нижче, щоб зануритись у мемну біржу."
)

HELP_TEXT = (
    "🧭 <b>Як грати</b>\n"
    "• <b>/cases</b> — переглянь усі кейси з шансами.\n"
    "• <b>/open PepeCase</b> або кнопка \"📦 Відкрити кейс\" — стартуй відкриття.\n"
    "• <b>/daily</b> — забирай щоденні бонуси.\n"
    "• <b>/inventory</b> — керуй колекцією та CP.\n"
    "• <b>/market</b> — купуй і продавай предмети, плати VUSDT.\n"
    "• <b>/send @друг 100</b> — поділись монетами (5% комісія).\n"
    "• <b>/trade @друг pepeblue#2442 for wojak#9911</b> — створити трейд-запит.\n"
    "• <b>/profile</b> — глянь баланс, CP і щоденний дохід.\n"
    "• <b>/leaderboard</b> — рейтинги VUSDT, CP та міфіків.\n"
    "• <b>/refer</b> — зароби на запрошеннях."
)

DAILY_ALREADY_CLAIMED = "⏳ Щоденний бонус уже активовано. Повертайся через кілька годин!"
DAILY_SUCCESS = "🎁 Щоденний бонус +{amount} VUSDT зараховано. Мемна імперія росте!"

BALANCE_TEMPLATE = "💸 На твоєму рахунку: <b>{vusdt}</b> • 🏆 CP: <b>{cp}</b>"

NO_CASE_FOUND = "😕 Кейс із таким кодом не знайдено. Скористайся /cases."
CASE_LOCKED_CP = "🔒 Цей кейс відкриється, коли назбираєш достатньо Collector Points."

OPEN_CASE_NOT_ENOUGH = "💸 Замало VUSDT для цього кейсу. Спробуй дешевший або зароби ще!"
OPEN_CASE_ANIMATION = [
    "🎞️ Розкручуємо барабан...",
    "✨ Сині іконки пролітають...",
    "🔥 Ще мить і дізнаємось результат!",
]
OPEN_CASE_SUCCESS = (
    "✅ <b>{case_name}</b> відкрито за {price} VUSDT!\n"
    "🏅 Трофей: {item_card}"
)

INVENTORY_EMPTY = "🪄 Інвентар порожній. Відкрий кейс або придбай щось на маркеті!"

REFERRAL_MESSAGE = (
    "🤝 Запрошуй друзів та отримуй винагороди!\n"
    "🔗 Посилання: {link}\n"
    "🎁 Бонус за друга: +{ref_bonus} VUSDT та +10% від його щоденних бонусів протягом 7 днів."
)

MARKET_EMPTY = "🛒 Активних лотів немає. Онови сторінку трохи згодом!"
MARKET_LISTING_CREATED = "📢 Лот #{listing_id} опубліковано на маркеті."
MARKET_PURCHASE_SUCCESS = "✅ Покупку завершено! Предмет уже у твоєму інвентарі."
MARKET_SELL_SUCCESS = "💰 Продаж успішний, VUSDT зараховано."

PROFILE_TEMPLATE = (
    "<b>{username}</b>\n"
    "Баланс: <b>{vusdt}</b>\n"
    "Collector Points: <b>{cp}</b>\n"
    "Щоденний приріст CP: <b>{daily_cp}</b>\n"
    "Ранг: <b>{rank}</b>\n"
    "Міфічних предметів: <b>{mythic}</b>"
)

LEADERBOARD_HEADER = "🏆 <b>Рейтинги Мемної Біржі</b>"
LEADERBOARD_SECTION = "{title}:\n{body}"

GENERIC_ERROR = "😔 Щось пішло не так. Команда вже працює над виправленням."
TRANSFER_SUCCESS = "💸 Переказано {net} VUSDT (комісія {fee} VUSDT)."
TRANSFER_RECIPIENT = "💌 Ти отримав {net} VUSDT від {sender}."
TRANSFER_NO_USER = "🙈 Не знайшов такого користувача. Попроси друга натиснути /start."
TRANSFER_SELF = "🤔 Не можна переказувати кошти самому собі."
TRANSFER_INVALID_AMOUNT = "🔢 Сума має бути додатним цілим числом."
TRADE_RECORDED = "🤝 Трейд-запит збережено. Надішли його другу, щоб він підтвердив у боті."
TRADE_USAGE = "Формат: /trade @друг pepeblue#2442 for wojak#9911"
QUESTS_PLACEHOLDER = "🎯 Квести з'являться у найближчому оновленні. Поки що збирай меми!"
