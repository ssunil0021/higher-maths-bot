from keyboards import home_keyboard, exam_keyboard, year_keyboard
from data import EXAMS, PDF_LINKS
#from user_stats import add_user, total_users
from config import ADMIN_IDS
#from user_stats import total_users
from safe_stats import add_user
from admin_stats import get_stats
from keyboards import csir_year_keyboard, csir_session_keyboard
from data import BOOKS
from keyboards import books_menu_keyboard
from difflib import SequenceMatcher



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

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


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

        elif data == "books":
            safe_edit(bot,call,"📚 <b>Books & PDFs</b>\n\nChoose option:",books_menu_keyboard())



        elif data == "booksearch":
            bot.send_message(call.message.chat.id,"🔍 Type book name / author / keyword:")

            bot.register_next_step_handler(call.message, handle_book_search)


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




def handle_book_search(msg):
    query = msg.text.lower().strip()
    results = []

    for book in BOOKS:
        text = (
            book["name"] + " " +
            book["author"] + " " +
            " ".join(book["keywords"])
        ).lower()

        score = similar(query, text)

        if score > 0.5 or query in text:
            results.append((score, book))

    if not results:
        bot.send_message(
            msg.chat.id,
            "❌ No matching books found.\nTry different spelling."
        )
        return

    results.sort(reverse=True, key=lambda x: x[0])

    for _, book in results[:5]:
        bot.send_message(
            msg.chat.id,
            f"📘 <b>{book['name']}</b>\n"
            f"👤 {book['author']}\n\n"
            f"⬇️ <a href='{book['link']}'>Download PDF</a>"
        )
