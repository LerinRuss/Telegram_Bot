from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram.update import Update
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup

import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def remove_keyboard(update: Update, ctx: CallbackContext):
    ctx.bot.send_message(chat_id=update.effective_chat.id,
                         text='Клавиатура должна удалиться, проверьте у себя, если не удалилась '
                         'то напишите.',
                         reply_markup=ReplyKeyboardRemove())


def start(update: Update, ctx: CallbackContext):
    ctx.bot.send_photo(update.effective_chat.id, open('res/Scene_1.png', 'rb'),
                       filename='scene_1', reply_markup=None)


updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('remove_keyboard', remove_keyboard))

updater.start_polling()
updater.idle()
