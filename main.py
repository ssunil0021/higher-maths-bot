from dotenv import load_dotenv
try:
    from rapidfuzz import fuzz
except:
    fuzz = None

load_dotenv()

import os
from flask import Flask, request
import telebot

from config import BOT_TOKEN, PARSE_MODE
from handlers import register_handlers

# create bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=PARSE_MODE)
register_handlers(bot)

# create server
app = Flask(__name__)

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("RAILWAY_PUBLIC_DOMAIN")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    print("Webhook set:", f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    app.run(host="0.0.0.0", port=8080)
