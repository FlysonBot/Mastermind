from dataclasses import dataclass

from mastermind.core.models.game_configuration import GameConfiguration
from mastermind.core.models.game_entities import GameEntities, create_game_entities
from mastermind.core.models.game_mode import GameMode  # type: ignore # noqa: F401
from mastermind.core.models.game_state import GameState
from mastermind.core.models.gameboard import GameBoard, create_empty_game_board


@dataclass
class Game:
    """Dataclass for a game.

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


def create_new_game(game_configuration: GameConfiguration) -> Game:
    """Creates a new game with the given game configuration.

    Args:
        game_configuration (GameConfiguration): The configuration of the game to be created.

    Returns:
        Game: The new game with the given configuration.

    Examples:
        >>> game_configuration = GameConfiguration(NUMBER_OF_COLORS=3, NUMBER_OF_DOTS=4, ATTEMPTS_ALLOWED=5, GAME_MODE=GameMode.PVP)
        >>> game = create_new_game(game_configuration)
        >>> isinstance(game, Game)
        True
        >>> game.game_board
        GameBoard(game_rounds=deque([]))
        >>> isinstance(game.game_configuration, GameConfiguration)
        True
        >>> isinstance(game.game_entities, GameEntities)
        True
        >>> game.game_state
        GameState(game_started=False, winner=None)
    """

    return Game(
        game_board=create_empty_game_board(),
        game_configuration=game_configuration,
        game_entities=create_game_entities(game_configuration.GAME_MODE),
        game_state=GameState(),
    )
