from typing import Any, Optional, Union, Dict

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext._basehandler import UT, RT, BaseHandler
from telegram.ext._utils.types import CCT
from telegram.ext import Updater, Application, CommandHandler, CallbackContext, CallbackQueryHandler

from game.game import Game, GameWord, Player, TurnResult
from game.game_dao import GameDao

from game.localization import *


REGEX_CONNECT = 'connect'
REGEX_PLAY = 'play'
REGEX_GOOD = 'keep_silent'
REGEX_BAD = 'testify'


class GameHandler(BaseHandler[Updater, CCT]):

    def __init__(self, handler: BaseHandler[Any, CCT], game_dao: GameDao):
        super(GameHandler, self).__init__(callback=handler.callback, block=handler.block)
        self.handler = handler
        self.game_dao = game_dao

    def check_update(self, update: object) -> Optional[Union[bool, object]]:
        return self.handler.check_update(update)

    async def handle_update(
            self,
            update: UT,
            application: "Application[Any, CCT, Any, Any, Any, Any]",
            check_result: object,
            context: CCT,
    ) -> RT:
        game = self.game_dao.get_or_create(update.effective_chat.id)
        context.update({'game': game})

        res = await self.handler.handle_update(update, application, check_result, context)

        self.game_dao.save(game, update.effective_chat.id)

        return res


async def create(update: Update, context: CallbackContext):
    game: Game = context.game

    if game.current_state is not game.IDLE:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_ERROR_TEXT)
        return

    game.create_room()

    keyboard_buttons = [[InlineKeyboardButton(CONNECT_BUTTON_TEXT, callback_data=REGEX_CONNECT)],
                        [InlineKeyboardButton(PLAY_BUTTON_TEXT, callback_data=REGEX_PLAY)]]
    keyboard = InlineKeyboardMarkup(keyboard_buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=CREATE_ROOM_TEXT, reply_markup=keyboard)


def play(update: Update, context: CallbackContext):
    game: Game = context.game

    if game.current_state is not game.CREATED:
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


def connect(update: Update, context: CallbackContext):
    game: Game = context.game

    if game.current_state is not game.CREATED:
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
    _say_answer(update, GameWord.GOOD, context.game)


def bad(update: Update, context: CallbackContext):
    _say_answer(update, GameWord.BAD, context.game)


def _say_answer(update: Update, answer: GameWord, game: Game):
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
        callback_query.edit_message_text(GAME_OVER_TEXT % {'stats': _build_stats(game.room)})
        game.stop()

        return

    callback_query.edit_message_text(SAY_NEXT_PAIR % {'pair': game.curr},
                                     reply_markup=callback_query.message.reply_markup)


def _build_stats(room: Dict[str, int]):
    msg = ''
    for (name, score) in room.items():
        msg += '%s: %s\n' % (name, score)

    return msg


async def force_stop(update: Update, context: CallbackContext):
    game: Game = context.game

    if game.current_state is game.IDLE:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=GAME_IS_NOT_PLAYED)
        return
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=GAME_OVER_TEXT % {'stats': _build_stats(game.room)})
    game.stop()


game_factory = GameDao()
handlers = [GameHandler(CommandHandler('create', create), game_factory),
            GameHandler(CommandHandler('force_stop', force_stop), game_factory),

            GameHandler(CallbackQueryHandler(connect, pattern=REGEX_CONNECT), game_factory),
            GameHandler(CallbackQueryHandler(play, pattern=REGEX_PLAY), game_factory),
            GameHandler(CallbackQueryHandler(good, pattern=REGEX_GOOD), game_factory),
            GameHandler(CallbackQueryHandler(bad, pattern=REGEX_BAD), game_factory)]
