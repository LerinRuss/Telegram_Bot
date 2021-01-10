from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from game.game import Game, TurnResult, GameWord
from localization import *

import logging
import os

START_COMMAND = 'start'
CREATE_COMMAND = 'create'
STOP_COMMAND = 'force_stop'

REGEX_CONNECT = 'connect'
REGEX_PLAY = 'play'

REGEX_BELIEVE = 'believe'
REGEX_LIE = 'lie'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = os.environ['TELEGRAM_BOT_TOKEN']
game = Game()


def start(update, context):
    keyboard_buttons = [[KeyboardButton(f'/{CREATE_COMMAND}')],
                        [KeyboardButton(f'/{STOP_COMMAND}')]]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=START_TEXT,
                             reply_markup=ReplyKeyboardMarkup(keyboard_buttons,
                                                              resize_keyboard=True,
                                                              one_time_keyboard=True))


def play(update, context):
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
    keyboard_buttons = [[InlineKeyboardButton(BELIEVE_BUTTON_TEXT, callback_data=REGEX_BELIEVE)],
                        [InlineKeyboardButton(LIE_BUTTON_TEXT, callback_data=REGEX_LIE)]]

    callback_query.edit_message_text(
        PLAY_TEXT % {
            'players': players_text,
            'pair': game.curr},
        reply_markup=InlineKeyboardMarkup(keyboard_buttons))


def create(update, context):
    if not game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_ERROR_TEXT)
        return

    game.create_room()

    keyboard_buttons = [[InlineKeyboardButton(CONNECT_BUTTON_TEXT, callback_data=REGEX_CONNECT)],
                        [InlineKeyboardButton(PLAY_BUTTON_TEXT, callback_data=REGEX_PLAY)]]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_TEXT, reply_markup=keyboard)


def connect(update, context):
    if not game.is__created:
        context.bot.send_message(chat_id=update.effective_chat.id, text=CONNECT_WARN_TEXT)
        return

    callback_query = update.callback_query
    callback_query.answer()

    user = callback_query.from_user.username
    if user in game.room:
        return

    game.join(user)
    callback_query.edit_message_text(
        CREATE_ROOM_TEXT + '\n' + CONNECTION_TEXT % {"players": ', '.join(list(game.room))},
        reply_markup=callback_query.message.reply_markup)


def believe(update, context):
    say_answer(update, context, GameWord.believe)


def lie(update, context):
    say_answer(update, context, GameWord.lie)


def say_answer(update, context, answer):
    callback_query = update.callback_query
    callback_query.answer()
    user_name = callback_query.from_user.username
    player = game.get_current_by_name(user_name)

    if player is None or player.answer is not None:
        return

    player.answer = answer
    turn_res = game.turn()

    if turn_res == TurnResult.keep_turn:
        callback_query.edit_message_text(f'{update.callback_query.message.text}\n'
                                         + ANSWERED_TEXT % {'player': user_name},
                                         reply_markup=callback_query.message.reply_markup)
        return

    if turn_res == TurnResult.game_ended:
        stop(callback_query)
        return

    callback_query.edit_message_text(SAY_NEXT_PAIR % {'pair': game.curr},
                                     reply_markup=callback_query.message.reply_markup)


def stop(callback_query):
    callback_query.edit_message_text(GAME_OVER_TEXT % {'stats': game.build_stats()})
    game.stop()


def force_stop(update, context):
    if game.is__idle:
        context.bot.send_message(chat_id=update.effective_chat.id, text=GAME_IS_NOT_PLAYED)
        return
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=GAME_OVER_TEXT % {'stats': game.build_stats()})
    game.stop()


updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler(START_COMMAND, start))
dispatcher.add_handler(CommandHandler(CREATE_COMMAND, create))
dispatcher.add_handler(CommandHandler(STOP_COMMAND, force_stop))
dispatcher.add_handler(CallbackQueryHandler(connect, pattern=REGEX_CONNECT))
dispatcher.add_handler(CallbackQueryHandler(play, pattern=REGEX_PLAY))
dispatcher.add_handler(CallbackQueryHandler(believe, pattern=REGEX_BELIEVE))
dispatcher.add_handler(CallbackQueryHandler(lie, pattern=REGEX_LIE))

updater.start_polling()
updater.idle()
