from keyboards import home_keyboard, exam_keyboard, year_keyboard
from data import EXAMS, PDF_LINKS

WELCOME_MSG = """📘 <b>Higher Maths PYQ Bot</b>

Authentic previous year papers for serious aspirants.

👇 Start below
"""

HELP_MSG = """ℹ️ <b>How to use</b>

1. Click PYQs  
2. Choose exam  
3. Select year  
4. Download PDF
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

    @bot.message_handler(commands=["start"])
    def start(msg):
        bot.send_message(msg.chat.id, WELCOME_MSG, reply_markup=home_keyboard())

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

        elif data == "pyqs":
            safe_edit(bot, call, "📂 <b>Select Exam</b>", exam_keyboard())

        elif data.startswith("exam|"):
            exam = data.split("|")[1]
            safe_edit(
                bot,
                call,
                f"📘 <b>{EXAMS[exam]}</b> – Select Year",
                year_keyboard(exam)
            )

        elif data.startswith("pdf|"):
            _, exam, year = data.split("|")
            link = PDF_LINKS.get(exam, {}).get(year)

            if not link:
                bot.send_message(call.message.chat.id, "❌ PDF not available")
            else:
                bot.send_message(
                    call.message.chat.id,
                    f"📘 <b>{EXAMS[exam]} – {year}</b>\n\n⬇️ <a href='{link}'>Download PDF</a>"
                )
