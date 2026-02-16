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
from keyboards import books_nav_keyboard, search_page_keyboard
from difflib import SequenceMatcher
try:
    from rapidfuzz import fuzz
except:
    fuzz = None
import time

import math
from keyboards import books_pagination_keyboard
from daily_data import get_daily_questions
import datetime


SEARCH_BOOK_MODE = set()
ADD_BOOK_MODE = set()

BOOK_ADD_STEP = {}
BOOK_WIZARD = {}

PAGE_SIZE = 10


SEARCH_QUERY = {}

ADMIN_IDS = 5615871641

WELCOME_MSG = """📘 <b>xMathematics</b>

Welcome! to xMathematics – A Serious Preparation Hub
Everything you need for competitive mathematics exams, carefully organized in one place.

CSIR-NET | GATE | NBHM | IIT JAM | ISI | CMI

What you get:
• Verified PYQs with answer keys
• Daily question practice with detailed solutions
• Organized book & PDF references
• Minimal, distraction-free experience

Coming soon:
• Video solutions for selected problems
• Expert guidance & strategy insights
"""


HELP_MSG = """ℹ️ How to Use xMathematics

A focused workspace for serious mathematics aspirants.

📂 PYQs

• Select exam
• Choose year
• Download paper & answer key

📘 Books & PDFs

• Subject-wise references
• Direct, clean downloads
• Curated academic material

🟢 Daily Question Practice

• Today’s Problem (morning release)
• Solution update (evening)
• Past questions — date-wise archive

🎯 Approach

Consistency > Intensity
Conceptual clarity > Random solving

Prepare with structure. Think deeply. Practice deliberately.
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

def send_books_page(bot, chat_id, subject, page, message_id=None):
    books = [b for b in get_books() if b.get("subject") == subject]

    if not books:
        bot.send_message(chat_id, "❌ No books found")
        return

    total_pages = math.ceil(len(books) / PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_books = books[start:end]

    text = f"📚 <b>{subject}</b>\n"
    text += f"<i>Page {page+1} / {total_pages}</i>\n\n"

    for book in page_books:
        title = book.get("book_name", "").strip()
        author = book.get("author", "").strip()
        link = book.get("pdf_link", "").strip()

        label = f"{title} — {author}" if author else title
        text += f"📘 <a href=\"{link}\">{label}</a>\n\n"

    if message_id:
        # 🔁 EDIT SAME MESSAGE
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=books_pagination_keyboard(subject, page, total_pages)
        )
    else:
        # 🆕 SEND NEW MESSAGE (first time)
        bot.send_message(
            chat_id,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=books_pagination_keyboard(subject, page, total_pages)
        )

def send_search_page(bot, chat_id, user_id, page, message_id=None):
    query = SEARCH_QUERY.get(user_id)

    if not query:
        bot.send_message(chat_id, "❌ Search expired. Please search again.")
        return

    all_books = get_books()
    results = []

    def sim(a, b):
        return SequenceMatcher(None, a, b).ratio()

    for book in all_books:
        text = f"{book.get('book_name','')} {book.get('author','')} {book.get('keywords','')}".lower()
        if query in text or sim(query, text) > 0.45:
            results.append(book)

    if not results:
        bot.send_message(chat_id, "❌ No matching books found.")
        return

    total_pages = math.ceil(len(results) / PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_books = results[start:end]

    text = f"🔍 <b>Search results for:</b> <i>{query}</i>\n"
    text += f"<i>Page {page+1} / {total_pages}</i>\n\n"

    for book in page_books:
        title = book.get("book_name", "").strip()
        author = book.get("author", "").strip()
        link = book.get("pdf_link", "").strip()

        label = f"{title} — {author}" if author else title
        text += f"📘 <a href=\"{link}\">{label}</a>\n\n"

    if message_id:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=search_page_keyboard(page, total_pages)
        )
    else:
        bot.send_message(
            chat_id,
            text,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=search_page_keyboard(page, total_pages)
        )

def send_past_page(bot, chat_id, page, message_id=None):
    import datetime
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

    PAGE_SIZE = 5

    questions = get_daily_questions()
    today = datetime.date.today().strftime("%Y-%m-%d")

    # remove today
    past = [q for q in questions if q.get("date") != today]

    # sort newest first
    past.sort(key=lambda x: x.get("date"), reverse=True)

    if not past:
        bot.send_message(chat_id, "❌ No past questions available.")
        return

    total_pages = (len(past) + PAGE_SIZE - 1) // PAGE_SIZE

    # safety
    if page < 0:
        page = 0
    if page >= total_pages:
        page = total_pages - 1

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    kb = InlineKeyboardMarkup(row_width=1)

    for q in past[start:end]:
        kb.add(
            InlineKeyboardButton(
                f"{q['day']}, {q['date']}",  # ← topic removed
                callback_data=f"view_question|{q['id']}"
            )
        )

    # pagination buttons
    nav = []
    if page > 0:
        nav.append(
            InlineKeyboardButton("⬅ Prev", callback_data=f"past_page|{page-1}")
        )

    if page < total_pages - 1:
        nav.append(
            InlineKeyboardButton("Next ➡", callback_data=f"past_page|{page+1}")
        )

    if nav:
        kb.row(*nav)

    kb.add(InlineKeyboardButton("🏠 Home", callback_data="home"))

    text = f"📂 <b>Past Daily Questions</b>\n\nPage {page+1} / {total_pages}"

    # 🔥 edit same message if message_id exists
    if message_id:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        bot.send_message(
            chat_id,
            text,
            reply_markup=kb,
            parse_mode="HTML"
        )

def register_handlers(bot):

    @bot.message_handler(func=lambda msg: msg.from_user.id in SEARCH_BOOK_MODE)
    def book_search_handler(msg):
       SEARCH_BOOK_MODE.discard(msg.from_user.id)

       query = msg.text.lower().strip()
       SEARCH_QUERY[msg.from_user.id] = query   # 🔥 save query

       send_search_page(
        bot,
        msg.chat.id,
        msg.from_user.id,
        page=0
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

             subject = slug.replace("_", " ").title()

             send_books_page(bot,call.message.chat.id,subject,page=0)







        elif data.startswith("bookpage|"):
             _, subject, page = data.split("|")

             send_books_page(bot,call.message.chat.id,subject.replace("_", " ").title(),int(page),message_id=call.message.message_id)





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

        elif data.startswith("searchpage|"):
             page = int(data.split("|")[1])

             send_search_page(bot,call.message.chat.id,call.from_user.id,page,message_id=call.message.message_id)


        elif data == "question_practice":
             from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
             kb = InlineKeyboardMarkup(row_width=1)
             kb.add(
        InlineKeyboardButton("🟢 Today's Question", callback_data="today_question"),
        InlineKeyboardButton("📂 Past Questions", callback_data="past_questions"),
        InlineKeyboardButton("🏠 Home", callback_data="home"))
             safe_edit(bot, call, "📘 <b>Question Practice</b>", kb)


        elif data == "today_question":

             import datetime
             import pytz

             from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

             questions = get_daily_questions()
             india = pytz.timezone("Asia/Kolkata")
             today = datetime.datetime.now(india)
             today_date = today.strftime("%Y-%m-%d")
             today_day = today.strftime("%A")
             current_hour = today.hour

             allowed_days = ["Monday", "Wednesday", "Friday"]

              # Find today's question
             today_q = next((q for q in questions if q.get("date") == today_date), None)

                # Sort all questions newest first
             questions_sorted = sorted(questions, key=lambda x: x.get("date"), reverse=True)

             # Latest past question
             last_q = next((q for q in questions_sorted if q.get("date") != today_date), None)


              # ❌ CASE 1 — Not Question Day
             if today_day not in allowed_days:

                text = f"""
📘 <b>Daily Question Practice</b>

Today is <b>{today_day}</b>.

🚫 <b>No new question today.</b>

Daily problems are released only on:

• Monday  
• Wednesday  
• Friday  

━━━━━━━━━━━━━━━
"""

                if last_q:
                   text += f"""
📂 <b>Practice the Latest Available Question:</b>

🗓 <b>{last_q['day']}, {last_q['date']}</b>
📖 <b>{last_q['topic']}</b>

📄 <a href="{last_q['question_link']}">Download Question PDF</a>
🧠 <a href="{last_q['solution_link']}">Download Solution PDF</a>

━━━━━━━━━━━━━━━
"""

                text += """
Want to explore older problems?
"""

                kb = InlineKeyboardMarkup(row_width=1)
                kb.add(InlineKeyboardButton("📂 Past Questions", callback_data="past_page|0"))
                kb.add(InlineKeyboardButton("🏠 Home", callback_data="home"))

                bot.send_message(call.message.chat.id, text,
                         parse_mode="HTML",
                         disable_web_page_preview=True,
                         reply_markup=kb)

                return


            # ❌ CASE 2 — Question Day but no entry in sheet
             if not today_q:
                bot.send_message(call.message.chat.id,
                         "❌ Question not uploaded yet.",
                         reply_markup=None)
                return


              # ✅ CASE 3 — Question Day (Before 7 PM)
             if current_hour < 19:

                text = f"""
📘 <b>Today's Question</b>

🗓 <b>{today_day}, {today_date}</b>
📖 <b>{today_q['topic']}</b>

📄 <a href="{today_q['question_link']}">Download Question PDF</a>

━━━━━━━━━━━━━━━

🕖 <b>Solution will be available at 7:00 PM.</b>

Stay consistent. Come back in the evening for the full explanation.

━━━━━━━━━━━━━━━

Missed previous questions?
"""

       # ✅ CASE 4 — After 7 PM
             else:

               text = f"""
📘 <b>Today's Question</b>

🗓 <b>{today_day}, {today_date}</b>
📖 <b>{today_q['topic']}</b>

📄 <a href="{today_q['question_link']}">Download Question PDF</a>
🧠 <a href="{today_q['solution_link']}">Download Solution PDF</a>

━━━━━━━━━━━━━━━

Want to practice older problems?
"""

             kb = InlineKeyboardMarkup(row_width=1)
             kb.add(InlineKeyboardButton("📂 Past Questions", callback_data="past_page|0"))
             kb.add(InlineKeyboardButton("🏠 Home", callback_data="home"))

             bot.send_message(call.message.chat.id,
                     text,
                     parse_mode="HTML",
                     disable_web_page_preview=True,
                     reply_markup=kb)


        elif data == "past_questions":
             send_past_page(bot, call.message.chat.id, 0)

        elif data.startswith("past_page|"):
             page = int(data.split("|")[1])
             send_past_page(bot, call.message.chat.id, page)

        elif data.startswith("view_question|"):
             qid = data.split("|")[1]

             questions = get_daily_questions()
             q = next((x for x in questions if str(x.get("id")) == qid), None)

             if not q:
                bot.answer_callback_query(call.id, "Question not found.")
                return

             text = f"""
📘 <b>{q['day']}, {q['date']}</b>
📚 <i>{q['topic']}</i>

────────────────

📄 <b>Question PDF</b>
<a href="{q['question_link']}">🔵 Download Question PDF</a>

🧠 <b>Solution PDF</b>
<a href="{q['solution_link']}">🔵 Download Solution PDF</a>

────────────────

Keep practicing consistently.  
Every problem strengthens your mathematical thinking.

Want to explore more past questions?
"""

             from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
             kb = InlineKeyboardMarkup(row_width=1)

             kb.add(InlineKeyboardButton("📂 Browse More Past Questions", callback_data="past_questions"))

             kb.add(InlineKeyboardButton("🏠 Home", callback_data="home"))

             bot.send_message(
        call.message.chat.id,
        text,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=kb
    )



