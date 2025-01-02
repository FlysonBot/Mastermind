from collections import deque

import pytest

from mastermind.server.database.enum import PlayerRole
from mastermind.server.database.models import Game, GameRound
from mastermind.server.services import (
    GameEndedException,
    GameNotStartedException,
    GameService,
    NoRedoAvailableException,
)


def test_add_round(game_service: GameService, game: Game) -> None:
    game_service.add_round((1, 2, 3, 4), (1, 0))
    assert game.game_board.game_rounds == deque(
        [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0))]
    )


def test_undo(game_service: GameService, game: Game) -> None:
    game_service.add_round((1, 2, 3, 4), (1, 0))
    game_service.undo()
    assert game.game_board.game_rounds == deque([])


def test_add_round_with_redo(game_service: GameService, game: Game) -> None:
    game_service.add_round((1, 2, 3, 4), (1, 0))
    game_service.undo()
    game_service.redo()
    assert game.game_board.game_rounds == deque(
        [GameRound(GUESS=(1, 2, 3, 4), FEEDBACK=(1, 0))]
    )


def test_add_round_after_end(game_service: GameService, game: Game) -> None:
    game.game_state.game_started = True
    game.game_state.winner = PlayerRole.CODE_SETTER
    with pytest.raises(GameEndedException):
        game_service.add_round((1, 2, 3, 4), (1, 0))


def test_undo_after_end(game_service: GameService, game: Game) -> None:
    game.game_state.game_started = True
    game.game_state.winner = PlayerRole.CODE_SETTER
    with pytest.raises(GameEndedException):
        game_service.undo()


def test_undo_before_start(game_service: GameService, game: Game) -> None:
    with pytest.raises(GameNotStartedException):
        game_service.undo()


def test_redo_before_start(game_service: GameService, game: Game) -> None:
    with pytest.raises(GameNotStartedException):
        game_service.redo()


def test_redo_without_undo(game_service: GameService, game: Game) -> None:
    game_service.add_round((1, 2, 3, 4), (1, 0))
    with pytest.raises(NoRedoAvailableException):
        game_service.redo()
