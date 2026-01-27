from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request
import telebot

from config import BOT_TOKEN, PARSE_MODE
from handlers import register_handlers

bot = telebot.TeleBot(BOT_TOKEN, parse_mode=PARSE_MODE)
register_handlers(bot)

app = Flask(__name__)

WEBHOOK_PATH = f"/{BOT_TOKEN}"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") + WEBHOOK_PATH

# Ensure polling is OFF
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def health():
    return "Bot is running", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
