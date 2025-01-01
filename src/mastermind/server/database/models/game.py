from attrs import Factory, define, field

from mastermind.server.database.models.game_configuration import GameConfiguration
from mastermind.server.database.models.game_entities import GameEntities
from mastermind.server.database.models.game_state import GameState
from mastermind.server.database.models.gameboard import GameBoard


@define
class Game:
    """Dataclass for a game.

    This class encapsulates all the essential information about a game, including the game board, configuration, entities, and current state.

    Attributes:
        game_board (GameBoard): The board representing the rounds and progress of the game.
        game_configuration (GameConfiguration): The settings that define how the game is played.
        game_entities (GameEntities): The participants involved in the game, such as players.
        game_state (GameState): The current state of the game, indicating whether it is ongoing, won, or lost.

    Examples:
        >>> from mastermind.server.database.enum.game_mode import GameMode
        >>> game_configuration = GameConfiguration(NUMBER_OF_COLORS=3, NUMBER_OF_DOTS=4, ATTEMPTS_ALLOWED=5, GAME_MODE=GameMode.PVP)
        >>> Game(game_configuration=game_configuration)
        Game(game_configuration=GameConfiguration(NUMBER_OF_COLORS=3, NUMBER_OF_DOTS=4, ATTEMPTS_ALLOWED=5, GAME_MODE=<GameMode.PVP: (<class 'mastermind.server.players.human_player.HumanSetter'>, <class 'mastermind.server.players.human_player.HumanBreaker'>)>), game_board=GameBoard(game_rounds=deque([])), game_state=GameState(game_started=False, winner=<PlayerRole.UNDETERMINED: 'UNDETERMINED'>), game_entities=GameEntities(Player(), Player()))
    """

    game_configuration: GameConfiguration
    game_board: GameBoard = Factory(GameBoard)
    game_state: GameState = Factory(GameState)
    game_entities: GameEntities = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.game_entities = GameEntities.from_game_mode(
            self.game_configuration.GAME_MODE
        )
