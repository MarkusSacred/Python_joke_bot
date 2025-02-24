from typing import Final
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import pyjokes

TOKEN: Final = "YOUR TOKEN"

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

0

ONE, ANOTHER_JOKE, END = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    keyboard = [[InlineKeyboardButton("Yes", callback_data=ONE)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id, text="Do you want to hear a joke?", reply_markup=reply_markup
    )

async def get_answer_yes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() 

    if query.data == str(ONE): 
        joke = pyjokes.get_joke()

        keyboard = [
            [
                InlineKeyboardButton("Do you want to hear another one?", callback_data=ANOTHER_JOKE),
                InlineKeyboardButton("No", callback_data=END)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(joke, reply_markup=reply_markup)

async def another_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == str(ANOTHER_JOKE):
        joke = pyjokes.get_joke()

        keyboard = [
            [
                InlineKeyboardButton("Do you want to hear another one?", callback_data=ANOTHER_JOKE),
                InlineKeyboardButton("No", callback_data=END)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(joke, reply_markup=reply_markup)
    else:
        await end_conversation(update, context)

async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    username = update.effective_chat.username
    chat_id = update.effective_chat.id

    await context.bot.send_message(
        chat_id=chat_id, text=f"Thank you {username} for using the Python Joke Bot!"
    )

if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Callback query handlers
    application.add_handler(CallbackQueryHandler(get_answer_yes, pattern="^" + str(ONE) + "$"))
    application.add_handler(CallbackQueryHandler(another_joke, pattern="^" + str(ANOTHER_JOKE) + "$"))
    application.add_handler(CallbackQueryHandler(end_conversation, pattern="^" + str(END) + "$"))

    application.run_polling()
