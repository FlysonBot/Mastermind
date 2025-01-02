from tempfile import TemporaryDirectory
from typing import Any, Generator

import pytest

from mastermind.server.database.enum import GameMode
from mastermind.server.database.models import Game, GameConfiguration
from mastermind.server.database.repository import GameRepository
from mastermind.server.services import GameboardService, GameService


@pytest.fixture
def game_configuration() -> GameConfiguration:
    return GameConfiguration(
        NUMBER_OF_COLORS=3,
        NUMBER_OF_DOTS=4,
        ATTEMPTS_ALLOWED=5,
        GAME_MODE=GameMode.PVP,
    )


@pytest.fixture
def game(game_configuration: GameConfiguration) -> Game:
    return Game(game_configuration=game_configuration)


@pytest.fixture
def gameboard_service(game: Game) -> GameboardService:
    return GameboardService(game.game_board)


@pytest.fixture
def game_service(game: Game, gameboard_service: GameboardService) -> GameService:
    return GameService(game, gameboard_service)


@pytest.fixture
def game_repository() -> Generator[GameRepository, Any, None]:
    with TemporaryDirectory() as temp_dir:
        yield GameRepository(temp_dir)
