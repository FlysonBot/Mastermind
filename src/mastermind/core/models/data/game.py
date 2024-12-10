from dataclasses import dataclass

from mastermind.core.models.data.game_configuration import GameConfiguration
from mastermind.core.models.data.game_entities import GameEntities
from mastermind.core.models.data.game_status import GameStatus
from mastermind.core.models.data.gameboard import GameBoard


@dataclass
class Game:
    """Dataclass for a game."""

    game_board: GameBoard
    game_configuration: GameConfiguration
    game_entities: GameEntities
    game_status: GameStatus
