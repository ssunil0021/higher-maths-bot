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
        buttons = [
            InlineKeyboardButton(year, callback_data=f"pdf|{exam}|{year}")
            for year in sorted(years, reverse=True)
        ]
        kb.add(*buttons)   # 🔥 THIS is the key line

    kb.add(
        InlineKeyboardButton("⬅️ Back", callback_data="pyqs"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb

def nbhm_category_keyboard():
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("📘 Combined (2023–Present)", callback_data="nbhmcat|combined"))
    kb.add(InlineKeyboardButton("🎓 Master's (2005–2022)", callback_data="nbhmcat|masters"))
    kb.add(InlineKeyboardButton("🎓 Doctoral (2005–2022)", callback_data="nbhmcat|doctoral"))

    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="pyqs"))
    return kb

def csir_year_keyboard():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=3)

    for year in sorted(PDF_LINKS["csir_net"].keys(), reverse=True):
        kb.add(InlineKeyboardButton(year, callback_data=f"csiryear|{year}"))

    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="pyqs"))
    return kb


def csir_session_keyboard(year):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=2)

    for session in PDF_LINKS["csir_net"][year]:
        kb.add(
            InlineKeyboardButton(
                f"{session} {year}",
                callback_data=f"csirsession|{year}|{session}"
            )
        )

    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="exam|csir_net"))
    return kb
