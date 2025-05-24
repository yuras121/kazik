import json
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
pip install aiogram==2.25.1

# Конфіг
BOT_TOKEN = "8034843480:AAFixXh46xpJ47sQWqc_uBA07pBK6ZfGrwQ"  # Отримайте у @BotFather
ADMIN_IDS = [000000000]   # Ваш Telegram ID
DATA_FILE = "data/users.json"

# Ініціалізація
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Клас для роботи з даними
class CasinoDB:
    def __init__(self):
        self.users = self._load_data()

    def _load_data(self):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def get_user(self, user_id: int):
        if str(user_id) not in self.users:
            self.users[str(user_id)] = {
                "balance": 500,
                "level": 1,
                "xp": 0,
                "bought_items": []
            }
        return self.users[str(user_id)]

db = CasinoDB()

# Слоти
SLOT_SYMBOLS = ["🍒", "💎", "7️⃣", "🍀", "🎲"]
SLOT_PAYOUTS = {
    ("🍒", "🍒", "🍒"): 10,
    ("💎", "💎", "💎"): 50,
    ("7️⃣", "7️⃣", "7️⃣"): 200,
    ("🍀", "🍀", "🍀"): 1000
}

# Рулетка
ROULETTE_NUMBERS = list(range(0, 37))
ROULETTE_RED = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Магазин
SHOP_ITEMS = {
    "1": {"name": "2x Бонус", "price": 300, "effect": "x2"},
    "2": {"name": "Щасливий день", "price": 1000, "effect": "daily_2x"}
}

# ================= КОМАНДИ =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = db.get_user(message.from_user.id)
    await message.reply(
        f"🎉 Вітаю в CasinoBot777!\n"
        f"💰 Баланс: {user['balance']} монет\n"
        f"💡 Доступні команди: /slots /roulette /daily /shop"
    )

@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    user = db.get_user(message.from_user.id)
    await message.reply(f"💰 Ваш баланс: {user['balance']} монет")

@dp.message_handler(commands=['daily'])
async def daily(message: types.Message):
    user = db.get_user(message.from_user.id)
    user['balance'] += 100 * user['level']
    db.save()
    await message.reply(f"🎁 Щоденний бонус: +{100 * user['level']} монет!")

@dp.message_handler(commands=['slots'])
async def slots(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user['balance'] < 50:
        await message.reply("🚫 Мінімальна ставка: 50 монет!")
        return

    user['balance'] -= 50
    result = random.choices(SLOT_SYMBOLS, weights=[40, 25, 15, 10, 5], k=3)
    win = 0

    for combo, multiplier in SLOT_PAYOUTS.items():
        if tuple(result) == combo:
            win = 50 * multiplier
            break

    user['balance'] += win
    db.save()
    
    slot_display = " | ".join(result)
    await message.reply(
        f"🎰 Слоти: {slot_display}\n"
        f"💸 {'Виграш: ' + str(win) if win else 'Програш...'}\n"
        f"💰 Баланс: {user['balance']}"
    )

@dp.message_handler(commands=['roulette'])
async def roulette(message: types.Message):
    try:
        _, color, bet = message.text.split()
        bet = int(bet)
    except:
        await message.reply("⚠️ Використання: /roulette [red/black/green] [ставка]")
        return

    user = db.get_user(message.from_user.id)
    if user['balance'] < bet:
        await message.reply("🚫 Недостатньо монет!")
        return

    number = random.choice(ROULETTE_NUMBERS)
    win = 0

    if color == "red" and number in ROULETTE_RED:
        win = bet * 2
    elif color == "black" and number not in ROULETTE_RED and number != 0:
        win = bet * 2
    elif color == "green" and number == 0:
        win = bet * 14

    user['balance'] += win - bet
    db.save()
    
    await message.reply(
        f"🎲 Рулетка: {number} {'🔴' if number in ROULETTE_RED else '⚫' if number !=0 else '🟢'}\n"
        f"💸 {'Виграш: ' + str(win) if win else 'Програш...'}\n"
        f"💰 Баланс: {user['balance']}"
    )

@dp.message_handler(commands=['shop'])
async def shop(message: types.Message):
    items = "\n".join([f"{id}. {item['name']} - {item['price']} монет" for id, item in SHOP_ITEMS.items()])
    await message.reply(f"🛒 Магазин:\n{items}\n\nКупити: /buy [id]")

# ================= АДМІН =================
@dp.message_handler(commands=['addcoins'])
async def addcoins(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        _, user_id, amount = message.text.split()
        user = db.get_user(int(user_id))
        user['balance'] += int(amount)
        db.save()
        await message.reply(f"✅ Додано {amount} монет юзеру {user_id}")
    except:
        await message.reply("⚠️ Використання: /addcoins [user_id] [amount]")

if __name__ == '__main__':
    print("🤑 Бот запущено!")
    executor.start_polling(dp)

