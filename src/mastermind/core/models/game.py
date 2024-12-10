from dataclasses import dataclass

from mastermind.core.models.game_configuration import GameConfiguration
from mastermind.core.models.game_entities import GameEntities
from mastermind.core.models.game_state import GameStatus
from mastermind.core.models.gameboard import GameBoard


@dataclass
class Game:
    """Dataclass for a game."""

    game_board: GameBoard
    game_configuration: GameConfiguration
    game_entities: GameEntities
    game_status: GameStatus
