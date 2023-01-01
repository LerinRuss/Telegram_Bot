from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.update import Update
from telegram.files.inputmedia import InputMediaPhoto
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from story import introduction, story, Scene, ImageSource

import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update: Update, ctx: CallbackContext):
    keyboard = [[InlineKeyboardButton('Стартуем', callback_data=0)]]

    image_source: ImageSource = introduction.image_source
    ctx.bot.send_photo(update.effective_chat.id,
                       image_source.source,
                       introduction.caption,
                       filename=image_source.file_name, reply_markup=InlineKeyboardMarkup(keyboard))


def next_scene(update: Update, ctx: CallbackContext):
    def inline_keyboard_factory(index: int, story: list[Scene]):
        return InlineKeyboardMarkup([[InlineKeyboardButton('➡', callback_data=index+1)]]) if index < len(story) - 1 \
            else None

    query = update.callback_query
    query.answer()

    index = int(query.data)
    scene: Scene = story[index]

    image_source: ImageSource = scene.image_source
    update.callback_query.edit_message_media(
        InputMediaPhoto(image_source.source, scene.caption, filename=image_source.file_name),
        reply_markup=inline_keyboard_factory(index, story))


updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(next_scene))

updater.start_polling()
updater.idle()
