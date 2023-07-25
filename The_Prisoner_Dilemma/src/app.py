from typing import Dict

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Dispatcher
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove, User
from telegram.update import Update
from game.game import Game, TurnResult, GameWord, Player
import game_factory
from localization import *

import logging
import os


REGEX_CONNECT = 'connect'
REGEX_PLAY = 'play'

REGEX_GOOD = 'keep_silent'
REGEX_BAD = 'testify'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['TELEGRAM_BOT_TOKEN']


def _build_stats(room: Dict[str, int]):
    msg = ''
    for (name, score) in room.items():
        msg += '%s: %s\n' % (name, score)

    return msg


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_TEXT)


def play(update: Update, context: CallbackContext):
    game: Game = game_factory.obtain_game(update.effective_chat.id)

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
    game: Game = game_factory.obtain_game(update.effective_chat.id)

    if not game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_ERROR_TEXT)
        return

    game.create_room()

    keyboard_buttons = [[InlineKeyboardButton(CONNECT_BUTTON_TEXT, callback_data=REGEX_CONNECT)],
                        [InlineKeyboardButton(PLAY_BUTTON_TEXT, callback_data=REGEX_PLAY)]]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_TEXT, reply_markup=keyboard)


def connect(update: Update, context: CallbackContext):
    game: Game = game_factory.obtain_game(update.effective_chat.id)

    if not game.is__created:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CONNECT_WARN_TEXT)
        return

    callback_query = update.callback_query
    callback_query.answer()

    user = callback_query.from_user
    user_id = user.username if user.username is not None else user.full_name

    if user_id in game.room:
        return

    game.join(user_id)
    callback_query.edit_message_text(
        CREATE_ROOM_TEXT + '\n' + CONNECTION_TEXT % {"players": ', '.join(list(game.room))},
        reply_markup=callback_query.message.reply_markup)


def good(update: Update, context: CallbackContext):
    _say_answer(update, GameWord.GOOD)


def bad(update: Update, context: CallbackContext):
    _say_answer(update, GameWord.BAD)


def _say_answer(update: Update, answer: GameWord):
    game: Game = game_factory.obtain_game(update.effective_chat.id)

    callback_query: CallbackQuery = update.callback_query
    callback_query.answer()
    user: str = callback_query.from_user
    user_id: str = user.username if user.username is not None else user.full_name
    player: Player = game.get_current_by_name(user_id)

    if player is None or player.answer is not None:
        return

    player.answer = answer
    turn_res: TurnResult = game.turn()

    if turn_res == TurnResult.keep_turn:
        callback_query.edit_message_text(f'{update.callback_query.message.text}\n'
                                         + ANSWERED_TEXT % {'player': user_id},
                                         reply_markup=callback_query.message.reply_markup)
        return

    if turn_res == TurnResult.game_ended:
        _stop(callback_query)
        return

    callback_query.edit_message_text(SAY_NEXT_PAIR % {'pair': game.curr},
                                     reply_markup=callback_query.message.reply_markup)


def _stop(callback_query: CallbackQuery):
    game: Game = game_factory.obtain_game(update.effective_chat.id)

    callback_query.edit_message_text(GAME_OVER_TEXT % {'stats': _build_stats(game.room)})
    game.stop()


def force_stop(update: Update, context: CallbackContext):
    game: Game = game_factory.obtain_game(update.effective_chat.id)

    if game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=GAME_IS_NOT_PLAYED)
        return
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=GAME_OVER_TEXT % {'stats': _build_stats(game.room)})
    game.stop()


updater = Updater(token=token, use_context=True)
dispatcher: Dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('create', create))
dispatcher.add_handler(CommandHandler('force_stop', force_stop))

dispatcher.add_handler(CallbackQueryHandler(connect, pattern=REGEX_CONNECT))
dispatcher.add_handler(CallbackQueryHandler(play, pattern=REGEX_PLAY))
dispatcher.add_handler(CallbackQueryHandler(good, pattern=REGEX_GOOD))
dispatcher.add_handler(CallbackQueryHandler(bad, pattern=REGEX_BAD))

updater.start_polling()
updater.idle()
