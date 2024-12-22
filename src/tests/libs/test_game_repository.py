from tempfile import TemporaryDirectory

import pytest

from mastermind.database.models.game import Game
from mastermind.database.models.game_configuration import GameConfiguration
from mastermind.database.models.game_mode import GameMode
from mastermind.database.libs import GameRepository


@pytest.fixture
def game_repository():
    with TemporaryDirectory() as temp_dir:
        yield GameRepository(temp_dir)


@pytest.fixture
def game():
    return Game(
        game_configuration=GameConfiguration(
            NUMBER_OF_COLORS=3,
            NUMBER_OF_DOTS=4,
            ATTEMPTS_ALLOWED=5,
            GAME_MODE=GameMode.PVP,
        )
    )


def test_add(game_repository: GameRepository, game: Game):
    uuid = game_repository.add(game)
    assert uuid in game_repository


def test_getitem(game_repository: GameRepository, game: Game):
    uuid = game_repository.add(game)
    assert game_repository[uuid] == game


def test_update_item(game_repository: GameRepository, game: Game):
    uuid = game_repository.add(game)
    new_game = Game(
        game_configuration=GameConfiguration(
            NUMBER_OF_COLORS=4,
            NUMBER_OF_DOTS=5,
            ATTEMPTS_ALLOWED=6,
            GAME_MODE=GameMode.PVE,
        )
    )
    game_repository[uuid] = new_game
    assert game_repository[uuid] == new_game


def test_delitem(game_repository: GameRepository, game: Game):
    uuid = game_repository.add(game)
    assert uuid in game_repository
    del game_repository[uuid]
    assert uuid not in game_repository


def test_len(game_repository: GameRepository, game: Game):
    # assert len(game_repository) == 0
    game_repository.add(game)
    assert len(game_repository) == 1
    game_repository.add(game)
    assert len(game_repository) == 2


def test_iter(game_repository: GameRepository, game: Game):
    game_repository.add(game)
    game_repository.add(game)
    assert all(_game == game_repository[uuid] for uuid, _game in game_repository)
    assert len(list(game_repository)) == 2
