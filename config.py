import os

ADMIN_IDS = {
    5615871641,      # tum     
    6524627058       # trusted user 2
}

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN not set")

PARSE_MODE = "HTML"   # 🔥 FIXED (was Markdown)
