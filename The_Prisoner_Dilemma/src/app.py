from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove, User
from telegram.update import Update
from game.game import Game, TurnResult, GameWord
from localization import *

import logging
import os


REGEX_CONNECT = 'connect'
REGEX_PLAY = 'play'

REGEX_GOOD = 'keep_silent'
REGEX_BAD = 'testify'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['TELEGRAM_BOT_TOKEN']
game: Game = Game()


def remove_keyboard(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(selective=True))


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_TEXT)


def play(update: Update, context: CallbackContext):
    if not game.is__created:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_WARN_TEXT)
        return

    callback_query = update.callback_query
    callback_query.answer()
    if len(game.room) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=NOT_ENOUGH_PLAYERS_TEXT)
        return

    game.play()

    players_text = ', '.join(list(game.room))
    keyboard_buttons = [[InlineKeyboardButton(BELIEVE_BUTTON_TEXT, callback_data=REGEX_GOOD)],
                        [InlineKeyboardButton(LIE_BUTTON_TEXT, callback_data=REGEX_BAD)]]

    callback_query.edit_message_text(
        PLAY_TEXT % {
            'players': players_text,
            'pair': game.curr},
        reply_markup=InlineKeyboardMarkup(keyboard_buttons))


def create(update: Update, context: CallbackContext):
    if not game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_ERROR_TEXT)
        return

    game.create_room()

    keyboard_buttons = [[InlineKeyboardButton(CONNECT_BUTTON_TEXT, callback_data=REGEX_CONNECT)],
                        [InlineKeyboardButton(PLAY_BUTTON_TEXT, callback_data=REGEX_PLAY)]]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_TEXT, reply_markup=keyboard)


def _get_user_identifier(user: User):
    username: str = user.username

    if username is None:
        return user.full_name

    return username


def connect(update: Update, context: CallbackContext):
    if not game.is__created:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CONNECT_WARN_TEXT)
        return

    callback_query = update.callback_query
    callback_query.answer()

    user_id = _get_user_identifier(callback_query.from_user)

    if user_id in game.room:
        return

    game.join(user_id)
    callback_query.edit_message_text(
        CREATE_ROOM_TEXT + '\n' + CONNECTION_TEXT % {"players": ', '.join(list(game.room))},
        reply_markup=callback_query.message.reply_markup)


def good(update: Update, context: CallbackContext):
    say_answer(update, context, GameWord.GOOD)


def bad(update: Update, context: CallbackContext):
    say_answer(update, context, GameWord.BAD)


def say_answer(update: Update, context: CallbackContext, answer: GameWord):
    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    user_id = _get_user_identifier(callback_query.from_user)
    player = game.get_current_by_name(user_id)

    if player is None or player.answer is not None:
        return

    player.answer = answer
    turn_res = game.turn()

    if turn_res == TurnResult.keep_turn:
        callback_query.edit_message_text(f'{update.callback_query.message.text}\n'
                                         + ANSWERED_TEXT % {'player': user_id},
                                         reply_markup=callback_query.message.reply_markup)
        return

    if turn_res == TurnResult.game_ended:
        stop(callback_query)
        return

    callback_query.edit_message_text(SAY_NEXT_PAIR % {'pair': game.curr},
                                     reply_markup=callback_query.message.reply_markup)


def stop(callback_query: CallbackQuery):
    callback_query.edit_message_text(GAME_OVER_TEXT % {'stats': game.build_stats()})
    game.stop()


def force_stop(update: Update, context: CallbackContext):
    if game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=GAME_IS_NOT_PLAYED)
        return
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=GAME_OVER_TEXT % {'stats': game.build_stats()})
    game.stop()


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('create', create))
dispatcher.add_handler(CommandHandler('force_stop', force_stop))
dispatcher.add_handler(CommandHandler('remove_keyboard', remove_keyboard))

dispatcher.add_handler(CallbackQueryHandler(connect, pattern=REGEX_CONNECT))
dispatcher.add_handler(CallbackQueryHandler(play, pattern=REGEX_PLAY))
dispatcher.add_handler(CallbackQueryHandler(good, pattern=REGEX_GOOD))
dispatcher.add_handler(CallbackQueryHandler(bad, pattern=REGEX_BAD))

updater.start_polling()
updater.idle()
