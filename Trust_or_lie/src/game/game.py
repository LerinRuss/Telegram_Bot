from statemachine import StateMachine, State
from enum import Enum

import random


class TurnResult(Enum):
    keep_turn = 1
    next_turn = 2
    game_ended = 3


class GameWord(Enum):
    believe = 1
    lie = 2


class Game(StateMachine):
    _idle = State('Idle', initial=True)
    _created = State('Created')
    _playing = State('Playing')

    _create = _idle.to(_created)
    _play = _created.to(_playing)
    _stop = _created.to(_idle) | _playing.to(_idle)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = dict()
        self.pairs = list()
        self.curr = None

    def create_room(self):
        self.clear()
        self._create()

    def play(self):
        self.pairs = pair_up(list(self.room))
        random.shuffle(self.pairs)
        self.curr = self.pairs.pop()
        self._play()

    def join(self, player_name):
        self.room[player_name] = 0

    def stop(self):
        self.clear()
        self._stop()

    def clear(self):
        self.room.clear()

    def get_current_by_name(self, player_name):
        if self.curr[0].name == player_name:
            return self.curr[0]

        if self.curr[1].name == player_name:
            return self.curr[1]

        return None

    def turn(self):
        first = self.curr[0]
        second = self.curr[1]

        if first.answer is None or second.answer is None:
            return TurnResult.keep_turn

        self.score_points(first, second)

        if len(self.pairs) == 0:
            return TurnResult.game_ended

        self.curr = self.pairs.pop()
        return TurnResult.next_turn

    def score_points(self, first, second):
        if first.answer == GameWord.lie and second.answer == GameWord.lie:
            return

        if first.answer == GameWord.believe and second.answer == GameWord.believe:
            self.room[first.name] = self.room[first.name] + 1
            self.room[second.name] = self.room[second.name] + 1

            return

        if first.answer == GameWord.lie:
            self.room[first.name] = self.room[first.name] + 2

        if second.answer == GameWord.lie:
            self.room[second.name] = self.room[second.name] + 2

    def build_stats(self):
        msg = ''
        for (name, score) in self.room.items():
            msg += '%s: %s\n' % (name, score)

        return msg


class Player:
    def __init__(self, name):
        self.name = name
        self.answer = None

    def __repr__(self):
        return self.name


def pair_up(players_arg):
    players = players_arg.copy()
    pairs = list()
    while players:
        last = players.pop()

        for curr in players:
            pairs.append((Player(last), Player(curr)))

    return pairs
