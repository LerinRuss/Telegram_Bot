from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from localization import *

import game.handlers as game_handlers
import logging
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['TELEGRAM_BOT_TOKEN']


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START_TEXT)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))

    for handler in game_handlers.handlers:
        application.add_handler(handler)

    application.run_polling()

