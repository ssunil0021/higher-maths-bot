from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import EXAMS, PDF_LINKS


def home_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📂 PYQs", callback_data="pyqs"),
        InlineKeyboardButton("📚 Books & PDFs", callback_data="books"),
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

def books_menu_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🔍 Search book", callback_data="booksearch"),
        InlineKeyboardButton("📂 Browse topics", callback_data="bookbrowse"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb

def books_nav_keyboard():
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🔍 Search again", callback_data="booksearch"),
        InlineKeyboardButton("📚 Books", callback_data="books"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb

def books_subject_keyboard(books):
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    kb = InlineKeyboardMarkup(row_width=2)

    subjects = sorted(
        set(b.get("subject") for b in books if b.get("subject"))
    )

    for subject in subjects:
        slug = subject.lower().replace(" ", "_")
        kb.add(
            InlineKeyboardButton(
                subject,
                callback_data=f"booksub|{slug}"
            )
        )

    kb.add(InlineKeyboardButton("⬅️ Back", callback_data="books"))
    return kb

def books_page_keyboard(subject, page, total_pages):
    kb = InlineKeyboardMarkup(row_width=2)

    if page > 0:
        kb.add(
            InlineKeyboardButton(
                "⬅️ Prev",
                callback_data=f"bookpage|{subject}|{page-1}"
            )
        )

    if page < total_pages - 1:
        kb.add(
            InlineKeyboardButton(
                "➡️ Next",
                callback_data=f"bookpage|{subject}|{page+1}"
            )
        )

    kb.add(
        InlineKeyboardButton("📚 Books", callback_data="books"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb


def books_pagination_keyboard(subject, page, total_pages):
    kb = InlineKeyboardMarkup(row_width=2)

    if page > 0:
        kb.add(
            InlineKeyboardButton(
                "⏮ Prev",
                callback_data=f"bookpage|{subject}|{page-1}"
            )
        )

    if page < total_pages - 1:
        kb.add(
            InlineKeyboardButton(
                "Next ⏭",
                callback_data=f"bookpage|{subject}|{page+1}"
            )
        )

    kb.add(
        InlineKeyboardButton("📚 Books", callback_data="books"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )

    return kb

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def search_page_keyboard(page, total_pages):
    kb = InlineKeyboardMarkup(row_width=2)

    buttons = []

    if page > 0:
        buttons.append(
            InlineKeyboardButton("⬅️ Prev", callback_data=f"searchpage|{page-1}")
        )

    if page < total_pages - 1:
        buttons.append(
            InlineKeyboardButton("➡️ Next", callback_data=f"searchpage|{page+1}")
        )

    if buttons:
        kb.add(*buttons)

    kb.add(
        InlineKeyboardButton("🔍 Search again", callback_data="booksearch"),
        InlineKeyboardButton("📚 Books", callback_data="books"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    )

    return kb

