from dotenv import load_dotenv
load_dotenv()

import telebot
from config import BOT_TOKEN, PARSE_MODE
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=PARSE_MODE)

register_handlers(bot)

print("🤖 Bot running...")

bot.infinity_polling(
    timeout=30,
    long_polling_timeout=30,
    skip_pending=True
)
