from statemachine import StateMachine, State
from enum import Enum
from typing import Dict, List, Tuple, Union
import random
import copy


class TurnResult(Enum):
    keep_turn = 1
    next_turn = 2
    game_ended = 3


class GameWord(Enum):
    GOOD = 1
    BAD = 2


class Player:
    def __init__(self, name: str, answer: Union[str, None] = None):
        self.name: str = name
        self.answer: Union[str, None] = answer

    def __repr__(self):
        return f"name is {self.name}, answer is {self.answer}"


class Game(StateMachine):
    IDLE = State('Idle', initial=True)
    CREATED = State('Created')
    PLAYING = State('Playing')

    _create = IDLE.to(CREATED)
    _play = CREATED.to(PLAYING)
    _stop = CREATED.to(IDLE) | PLAYING.to(IDLE)

    def __init__(self,
                 room: Union[Dict[str, int], None] = None,
                 pairs: List[Tuple[Player, Player]] = None,
                 curr: Union[Tuple[Player, Player], None] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if room is None:
            room = dict()

        if pairs is None:
            pairs = list()

        self.room: Dict[str, int] = copy.deepcopy(room)
        self.pairs: List[Tuple[Player, Player]] = copy.deepcopy(pairs)
        self.curr: Union[Tuple[Player, Player], None] = curr

    def create_room(self):
        self.clear()
        self._create()

    def play(self):
        self.pairs: List[Tuple[Player, Player]] = pair_up(list(self.room))
        random.shuffle(self.pairs)
        self.curr: Union[Tuple[Player, Player], None] = self.pairs.pop()
        self._play()

    def join(self, player_name: str):
        self.room[player_name] = 0

    def stop(self):
        self.clear()
        self._stop()

    def clear(self):
        self.room.clear()

    def get_current_by_name(self, player_name: str) -> Union[Player, None]:
        if self.curr[0].name == player_name:
            return self.curr[0]

        if self.curr[1].name == player_name:
            return self.curr[1]

        return None

    def turn(self) -> TurnResult:
        first: Player = self.curr[0]
        second: Player = self.curr[1]

        if first.answer is None or second.answer is None:
            return TurnResult.keep_turn

        self.score_points(first, second)

        if len(self.pairs) == 0:
            return TurnResult.game_ended

        self.curr = self.pairs.pop()
        return TurnResult.next_turn

    def score_points(self, first: Player, second: Player):
        if first.answer == GameWord.BAD and second.answer == GameWord.BAD:
            self.room[first.name] = self.room[first.name] + 24
            self.room[second.name] = self.room[second.name] + 24
            return

        if first.answer == GameWord.GOOD and second.answer == GameWord.GOOD:
            self.room[first.name] = self.room[first.name] + 6
            self.room[second.name] = self.room[second.name] + 6

            return

        if first.answer == GameWord.GOOD:
            self.room[first.name] = self.room[first.name] + 120

        if second.answer == GameWord.GOOD:
            self.room[second.name] = self.room[second.name] + 120


def pair_up(players_arg: List[str]) -> List[Tuple[Player, Player]]:
    players: List[str] = players_arg.copy()
    pairs: List[Tuple[Player, Player]] = list()
    while players:
        last: str = players.pop()

        for curr in players:
            pairs.append((Player(last), Player(curr)))

    return pairs
