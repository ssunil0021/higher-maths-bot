from keyboards import home_keyboard, exam_keyboard, year_keyboard
from data import EXAMS, PDF_LINKS
#from user_stats import add_user, total_users
from config import ADMIN_IDS
#from user_stats import total_users
from safe_stats import add_user
from admin_stats import get_stats
from keyboards import csir_year_keyboard, csir_session_keyboard, books_subject_keyboard
from books_data import get_books
from keyboards import books_menu_keyboard
from keyboards import books_nav_keyboard
from difflib import SequenceMatcher
try:
    from rapidfuzz import fuzz
except:
    fuzz = None
import time

SEARCH_BOOK_MODE = set()
ADD_BOOK_MODE = set()

BOOK_ADD_STEP = {}
BOOK_WIZARD = {}


ADMIN_IDS = 5615871641

WELCOME_MSG = """📘 <b>Higher Maths PYQs</b>

Welcome! 👋  
This bot helps you prepare for higher mathematics exams in one place.

Available now:
• Previous year question papers (PYQs)  
• Answer keys (where available)  
• Clean and fast downloads  

Coming soon:
• Detailed solutions of PYQs  
• Expert guidance for exams  
• Best video suggestions to learn topics  
• Book PDFs & references  
• Short notes for revision  

👇 Start by selecting your exam below
"""


HELP_MSG = """ℹ️ <b>How to use</b>

1️⃣ Click PYQs  
2️⃣ Choose exam  
3️⃣ Select category (if shown)  
4️⃣ Select year  
5️⃣ Download PDFs  

📌 Tip: Practice PYQs year-wise for better understanding.
"""






def safe_edit(bot, call, text, kb):
    try:
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=kb
        )
    except:
        pass


def register_handlers(bot):

    @bot.message_handler(func=lambda msg: msg.from_user.id in SEARCH_BOOK_MODE)
    def book_search_handler(msg):
        SEARCH_BOOK_MODE.discard(msg.from_user.id)

        loading = bot.send_message(msg.chat.id, "⏳ Searching books…")

        query = msg.text.lower().strip()
        results = []

        from difflib import SequenceMatcher
        def sim(a, b):
            return SequenceMatcher(None, a, b).ratio()

        for book in get_books():
            text = f"{book.get('book_name','')} {book.get('author','')} {book.get('keywords','')}".lower()
            if sim(query, text) > 0.45 or query in text:
               results.append(book)

        bot.delete_message(msg.chat.id, loading.message_id)

        if not results:
           bot.send_message(
            msg.chat.id,
            "❌ No matching books found.\nTry different spelling.",
            reply_markup=books_nav_keyboard()
        )
           return

        for book in results[:5]:
            bot.send_message(
            msg.chat.id,
            f"📘 <b>{book['book_name']}</b>\n"
            f"👤 {book['author']}\n"
            f"⬇️ <a href='{book['pdf_link']}'>Download PDF</a>"
        )

        bot.send_message(
        msg.chat.id,
        "✨ <b>What next?</b>",
        reply_markup=books_nav_keyboard()
    )

    @bot.message_handler(func=lambda m: m.from_user.id in ADD_BOOK_MODE)
    def receive_book(msg):
        ADD_BOOK_MODE.discard(msg.from_user.id)

        parts = msg.text.split("|")
        if len(parts) != 5:
           bot.send_message(msg.chat.id, "❌ Invalid format")
           return

        book = {
        "book_name": parts[0].strip(),
        "author": parts[1].strip(),
        "subject": parts[2].strip(),
        "keywords": parts[3].strip(),
        "pdf_link": parts[4].strip(),
        "status": "approved",
        "uploaded_by": "admin"
        }

        import requests, os
        requests.post(os.getenv("BOOKS_SHEET_URL"), json=book)

        bot.send_message(msg.chat.id, "✅ Book added successfully") 
    
    
    @bot.message_handler(commands=["addbook"])
    def add_book_start(msg):
        if msg.from_user.id != ADMIN_IDS:
           return

        uid = msg.from_user.id
        BOOK_ADD_STEP[uid] = 1
        BOOK_WIZARD[uid] = {}

        bot.send_message(msg.chat.id,"📘 <b>Add New Book</b>\n\n""Step 1️⃣: Send <b>Book Name</b>")

    @bot.message_handler(func=lambda m: m.from_user.id in BOOK_ADD_STEP)
    def add_book_wizard(msg):
        uid = msg.from_user.id
        step = BOOK_ADD_STEP[uid]

        if step == 1:
           BOOK_WIZARD[uid]["book_name"] = msg.text.strip()
           BOOK_ADD_STEP[uid] = 2
           bot.send_message(msg.chat.id, "Step 2️⃣: Send <b>Author Name</b>")

        elif step == 2:
           BOOK_WIZARD[uid]["author"] = msg.text.strip()
           BOOK_ADD_STEP[uid] = 3
           bot.send_message(msg.chat.id, "Step 3️⃣: Send <b>Subject</b>\n(e.g. Linear Algebra)")

        elif step == 3:
           BOOK_WIZARD[uid]["subject"] = msg.text.strip()
           BOOK_ADD_STEP[uid] = 4
           bot.send_message(msg.chat.id, "Step 4️⃣: Send <b>Keywords</b>\n(comma separated)")

        elif step == 4:
           BOOK_WIZARD[uid]["keywords"] = msg.text.strip()
           BOOK_ADD_STEP[uid] = 5
           bot.send_message(msg.chat.id,"Step 5️⃣: Send <b>Exam tags</b>\n(e.g. csir,gate,jam)")

        elif step == 5:
           BOOK_WIZARD[uid]["exam_tags"] = msg.text.strip()
           BOOK_ADD_STEP[uid] = 6
           bot.send_message(msg.chat.id, "Step 6️⃣: Send <b>PDF Download Link</b>")

        elif step == 6:
           BOOK_WIZARD[uid]["pdf_link"] = msg.text.strip()

           book = BOOK_WIZARD[uid]
           book["status"] = "approved"
           book["uploaded_by"] = "admin"

           import requests, os
           r = requests.post(os.getenv("BOOKS_SHEET_URL"), json=book)

           bot.send_message(
            msg.chat.id,
            "✅ <b>Book added successfully!</b>\n\n"
            f"📘 {book['book_name']}\n"
            f"👤 {book['author']}\n"
            f"📂 {book['subject']}")

           BOOK_ADD_STEP.pop(uid, None)
           BOOK_WIZARD.pop(uid, None)


    @bot.message_handler(commands=["debugbooks"])
    def debug_books(msg):
        books = get_books()
        bot.send_message(msg.chat.id, f"Books count: {len(books)}")
        if books:
           bot.send_message(msg.chat.id, str(books[0]))


    

     


    @bot.message_handler(commands=["start"])
    def start(msg):
        add_user(msg.from_user)
        bot.send_message(msg.chat.id, WELCOME_MSG, reply_markup=home_keyboard())



    @bot.message_handler(commands=["stats"])
    def stats(msg):
        if msg.from_user.id != ADMIN_IDS:
             return

        s = get_stats()

        bot.send_message(
        msg.chat.id,
        f"📊 Bot Stats\n\n"
        f"👥 Total users: {s.get('total', 0)}\n"
        f"🆕 New today: {s.get('new_today', 0)}\n"
        f"📅 Active today: {s.get('active_today', 0)}"
        )




    @bot.message_handler(commands=["help"])
    def help_cmd(msg):
        bot.send_message(msg.chat.id, HELP_MSG, reply_markup=home_keyboard())

    @bot.callback_query_handler(func=lambda c: True)
    def callback_router(call):
        bot.answer_callback_query(call.id)
        data = call.data

        if data == "home":
            safe_edit(bot, call, WELCOME_MSG, home_keyboard())

        elif data == "help":
            safe_edit(bot, call, HELP_MSG, home_keyboard())

        elif data == "bookbrowse":
            books = get_books()
            safe_edit(
        bot,
        call,
        "📂 <b>Select subject</b>",
        books_subject_keyboard(books)
    )



        elif data.startswith("booksub|"):
             slug = data.split("|")[1]

             def normalize(s):
                 return s.lower().replace(" ", "_")

             books = [
                 b for b in get_books()
                 if normalize(b.get("subject", "")) == slug
             ]

             if not books:
                bot.send_message(call.message.chat.id, "❌ No books found")
                return

             text = f"📚 <b>{slug}</b>\n\n"

             for book in books[:10]:
                 text += (
            f"📘 <a href='{book['pdf_link']}'>"
            f"{book['book_name']} — {book['author']}"
            f"</a>\n"
        )

             bot.send_message(call.message.chat.id, text, parse_mode='HTML')

             bot.send_message(call.message.chat.id,"✨ More options:",reply_markup=books_nav_keyboard())





        elif data.startswith("bookpage|"):
            _, subject, page = data.split("|")
            page = int(page)
            PAGE_SIZE = 10

            books = [b for b in get_books() if b.get("subject") == subject]

            total_pages = (len(books) + PAGE_SIZE - 1) // PAGE_SIZE
            start = page * PAGE_SIZE
            end = start + PAGE_SIZE

            text = f"📚 <b>{subject}</b>\n\n"

            for b in books[start:end]:
                text += (
            f"📘 <b>{b['book_name']}</b>\n"
            f"👤 {b['author']}\n"
            f"⬇️ <a href='{b['pdf_link']}'>Download PDF</a>\n\n")

            from keyboards import books_page_keyboard
            bot.edit_message_text(text,call.message.chat.id,call.message.message_id,reply_markup=books_page_keyboard(subject, page, total_pages))




        elif data == "books":
            safe_edit(bot,call,"📚 <b>Books & PDFs</b>\n\n"
    "• Search any book\n"
    "• Find PDFs instantly\n"
    "• Typo-tolerant smart search\n\n"
    "Choose an option below 👇",books_menu_keyboard())


        elif data == "booksearch":
             SEARCH_BOOK_MODE.add(call.from_user.id)
             bot.send_message(
        call.message.chat.id,
        "🔍 <b>Search books & PDFs</b>\n\n"
        "Type book name, author, or topic.\n"
        "<i>(typos also work)</i>"
    )




        elif data == "pyqs":
            safe_edit(bot, call, """📂 <b>Select Exam</b>

All PYQs here are carefully organised year-wise for easy practice.
Choose the exam you are preparing for.

"""
, exam_keyboard())
            
        elif data == "exam|csir_net":
             safe_edit(bot,call,"""📘 <b>CSIR-NET</b>\n\nSelect a year to download:
• Question paper  
• Answer key (if available):""",csir_year_keyboard())

        elif data.startswith("exam|"):
             exam = data.split("|")[1]

             if exam == "nbhm":
                 from keyboards import nbhm_category_keyboard
                 safe_edit(bot,call,"""📘 <b>NBHM</b>

From 2023 onwards, the exam is combined.
Before that, Master's and Doctoral were separate.

Select the category below:
"""
,nbhm_category_keyboard())
             else:
                 safe_edit(bot,call,f"""📘 <b>{EXAMS[exam]}</b>

Select a year to download:
• Question paper  
• Answer key (if available)

"""
,year_keyboard(exam))

        elif data.startswith("pdf|"):
            _, exam, year = data.split("|")

            data_year = PDF_LINKS.get(exam, {}).get(year)

            if not data_year:
               bot.send_message(call.message.chat.id, "❌ PDF not available")
               return

            text = f"📘 <b>{EXAMS[exam]} – {year}</b>\n\n"

            text += f"📄 <b>Question Paper</b>\n"
            text += f"⬇️ <a href='{data_year['question']}'>Download</a>\n\n"

            if "answer" in data_year:
                text += f"📝 <b>Answer Key</b>\n"
                text += f"⬇️ <a href='{data_year['answer']}'>Download</a>"
            else:
                text += "📝 <b>Answer Key</b>\n❌ Not available"
            text += """\n\n📌 More resources will be added soon.Update will be posted here:https://t.me/HigherMathematicsBot1 Stay connected!"""

            bot.send_message(call.message.chat.id, text)

        elif data.startswith("nbhmcat|"):
            category = data.split("|")[1]

            years = PDF_LINKS["nbhm"][category]["years"]

            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
            kb = InlineKeyboardMarkup(row_width=3)

            buttons = [
                 InlineKeyboardButton(
                    year,
                    callback_data=f"nbhmpdf|{category}|{year}"
                 )
                 for year in sorted(years, reverse=True)
            ]

            kb.add(*buttons)
            kb.add(InlineKeyboardButton("⬅️ Back", callback_data="exam|nbhm"))

            safe_edit(bot,call,f"""📅 <b>{PDF_LINKS['nbhm'][category]['label']}</b>

Select a year to download:
• Question paper  
• Answer key
"""
, kb)

        elif data.startswith("nbhmpdf|"):
             _, category, year = data.split("|")

             data_year = PDF_LINKS["nbhm"][category]["years"][year]

             text = f"📘 <b>NBHM – {year}</b>\n\n"
             text += f"📄 <b>Question Paper</b>\n⬇️ <a href='{data_year['question']}'>Download</a>\n\n"

             if "answer" in data_year:
                 text += f"📝 <b>Answer Key</b>\n⬇️ <a href='{data_year['answer']}'>Download</a>"
             else:
                 text += "📝 <b>Answer Key</b>\n❌ Not available"
             text += """\n\n📌 More resources will be added soon.Update will be posted here:https://t.me/HigherMathematicsBot1
             
             Stay connected!"""


             bot.send_message(call.message.chat.id, text)

        

        elif data.startswith("csiryear|"):
             year = data.split("|")[1]
             safe_edit(bot,call,f"📅 <b>{year}</b>\n\nSelect session:",csir_session_keyboard(year))

        elif data.startswith("csirsession|"):
             _, year, session = data.split("|")
             data_pdf = PDF_LINKS["csir_net"][year][session]

             text = f"""📘 <b>CSIR-NET {session} {year}</b>

📄 Question Paper
⬇️ <a href="{data_pdf['question']}">Download</a>

📝 Answer Key
⬇️ <a href="{data_pdf['answer']}">Download</a>
"""

             bot.send_message(call.message.chat.id, text)



    

