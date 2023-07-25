from game.game import Game

_id_game_mapping = dict()


def obtain_game(id: int) -> Game:
    return _id_game_mapping.setdefault(id, Game())
