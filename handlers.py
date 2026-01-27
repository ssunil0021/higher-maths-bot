from keyboards import home_keyboard, exam_keyboard, year_keyboard
from data import EXAMS, PDF_LINKS

WELCOME_MSG = """📘 *Higher Maths PYQ Bot*

Authentic previous year papers for serious aspirants.

👇 Start below
"""

HELP_MSG = """ℹ️ *How to use*

1. Click PYQs  
2. Choose exam  
3. Select year  
4. Download PDF
"""


def register_handlers(bot):

    @bot.message_handler(commands=["start"])
    def start(msg):
        bot.send_message(msg.chat.id, WELCOME_MSG, reply_markup=home_keyboard())

    @bot.message_handler(commands=["help"])
    def help_cmd(msg):
        bot.send_message(msg.chat.id, HELP_MSG, reply_markup=home_keyboard())

    @bot.callback_query_handler(func=lambda c: True)
    def callback_router(call):
        try:
            bot.answer_callback_query(call.id)
            data = call.data

            if data == "home":
                bot.edit_message_text(WELCOME_MSG, call.message.chat.id,
                                      call.message.message_id, reply_markup=home_keyboard())

            elif data == "help":
                bot.edit_message_text(HELP_MSG, call.message.chat.id,
                                      call.message.message_id, reply_markup=home_keyboard())

            elif data == "pyqs":
                bot.edit_message_text("📂 *Select Exam*", call.message.chat.id,
                                      call.message.message_id, reply_markup=exam_keyboard())

            elif data.startswith("exam|"):
                exam = data.split("|")[1]
                bot.edit_message_text(
                    f"📘 *{EXAMS[exam]}* – Select Year",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=year_keyboard(exam)
                )

            elif data.startswith("pdf|"):
                _, exam, year = data.split("|")
                link = PDF_LINKS.get(exam, {}).get(year)

                if not link:
                    bot.send_message(call.message.chat.id, "❌ PDF not available")
                else:
                    bot.send_message(
                        call.message.chat.id,
                        f"📘 *{EXAMS[exam]} – {year}*\n\n⬇️ [Download PDF]({link})"
                    )

        except Exception as e:
            print("ERROR:", e)
            bot.send_message(call.message.chat.id, "⚠️ Internal error. Try again later.")
