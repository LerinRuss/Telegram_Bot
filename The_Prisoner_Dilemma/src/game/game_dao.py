from typing import Union, Dict, List, Tuple

from redis_om import JsonModel, EmbeddedJsonModel, NotFoundError
from .game import Game, Player


class RedisPlayer(EmbeddedJsonModel):
    name: str
    answer: Union[str, None]


class RedisGame(JsonModel):
    class Meta:
        model_key_prefix = 'prisoner-dilemma-bot'

    current_state_value: str
    room: Union[Dict[str, int], None]
    pairs: List[Tuple[RedisPlayer, RedisPlayer]]
    curr: Union[Tuple[RedisPlayer, RedisPlayer], None]


class RedisGameMapper:
    def map_to_game(self, redis_game: RedisGame) -> Game:
        pairs = [(self._map_redis_player_to_game_player(pair[0]), self._map_redis_player_to_game_player(pair[1]))
                 for pair in redis_game.pairs]
        curr = (self._map_redis_player_to_game_player(redis_game.curr[0]),
                self._map_redis_player_to_game_player(redis_game.curr[1])) \
            if redis_game.curr \
            else None
        game = Game(redis_game.room, pairs, curr)
        game.current_state_value = redis_game.current_state_value

        return game

    def map_to_redis(self, game: Game) -> RedisGame:
        redis_pairs = [
            (self._map_game_player_to_redis_player(pair[0]), self._map_game_player_to_redis_player(pair[1]))
            for pair in game.pairs]
        curr = (self._map_game_player_to_redis_player(game.curr[0]),
                self._map_game_player_to_redis_player(game.curr[1])) \
            if game.curr \
            else None

        return RedisGame(
            current_state_value=game.current_state_value,
            room=game.room,
            pairs=redis_pairs,
            curr=curr)

    def _map_redis_player_to_game_player(self, redis_player: RedisPlayer) -> Player:
        return Player(redis_player.name, redis_player.answer)

    def _map_game_player_to_redis_player(self, player: Player) -> RedisPlayer:
        return RedisPlayer(name=player.name, answer=player.answer)


class GameDao:
    def __init__(self, mapper: RedisGameMapper = RedisGameMapper()):
        self._mapper: RedisGameMapper = mapper

    def get_or_create(self, id: int) -> Game:
        try:
            redis_game = RedisGame.get(id)
            game = self._mapper.map_to_game(redis_game)

            return game
        except NotFoundError:
            game = Game()
            self.save(game, id)

            return game

    def save(self, game: Game, id: int):
        redis_game = self._mapper.map_to_redis(game)
        redis_game.pk = id
        four_hours_in_seconds = 14_400
        redis_game.expire(four_hours_in_seconds)
        redis_game.save()
