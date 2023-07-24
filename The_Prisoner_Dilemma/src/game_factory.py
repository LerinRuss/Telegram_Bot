from game.game import Game

_game: Game = Game()


def obtain_game() -> Game:
    return _game
