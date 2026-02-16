import os

ADMIN_IDS = 5615871641
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@xMathematics01"


if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN not set")

PARSE_MODE = "HTML"   # 🔥 FIXED (was Markdown)
