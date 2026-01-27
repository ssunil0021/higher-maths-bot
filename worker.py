import os, redis, telebot
from handlers import register_handlers
from config import BOT_TOKEN, PARSE_MODE

r = redis.from_url(os.getenv("REDIS_URL"))

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=PARSE_MODE)
register_handlers(bot)

print("Worker started...")

while True:
    _, data = r.brpop("updates")
    update = telebot.types.Update.de_json(data.decode("utf-8"))
    bot.process_new_updates([update])
