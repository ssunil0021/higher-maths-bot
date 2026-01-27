from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import EXAMS, PDF_LINKS


def home_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📂 PYQs", callback_data="pyqs"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    )
    return kb


def exam_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    for k, v in EXAMS.items():
        kb.add(InlineKeyboardButton(v, callback_data=f"exam|{k}"))
    kb.add(InlineKeyboardButton("🏠 Home", callback_data="home"))
    return kb


def year_keyboard(exam):
    kb = InlineKeyboardMarkup(row_width=3)
    years = PDF_LINKS.get(exam, {})

    if not years:
        kb.add(InlineKeyboardButton("❌ No PDFs", callback_data="none"))
    else:
        for year in sorted(years, reverse=True):
            kb.add(InlineKeyboardButton(year, callback_data=f"pdf|{exam}|{year}"))

    kb.add(
        InlineKeyboardButton("⬅️ Back", callback_data="pyqs"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb
