from dataclasses import dataclass

from mastermind.core.models.game_configuration import GameConfiguration
from mastermind.core.models.game_entities import GameEntities
from mastermind.core.models.game_state import GameState
from mastermind.core.models.gameboard import GameBoard


@dataclass
class Game:
    """
    Dataclass for a game.

    This class encapsulates all the essential information about a game, including the game board, configuration, entities, and current state.

    Attributes:
        game_board (GameBoard): The board representing the rounds and progress of the game.
        game_configuration (GameConfiguration): The settings that define how the game is played.
        game_entities (GameEntities): The participants involved in the game, such as players.
        game_state (GameState): The current state of the game, indicating whether it is ongoing, won, or lost.
    """

    game_board: GameBoard
    game_configuration: GameConfiguration
    game_entities: GameEntities
    game_state: GameState
