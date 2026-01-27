from dotenv import load_dotenv
load_dotenv()
from config import BOT_TOKEN


import telebot
from config import BOT_TOKEN, PARSE_MODE
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=PARSE_MODE)
register_handlers(bot)

print("🤖 Bot running...")
bot.infinity_polling(skip_pending=True)
