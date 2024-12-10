from dataclasses import dataclass

from mastermind.core.models.game_mode import GameMode


@dataclass
class GameConfiguration:
    """
    Dataclass for the configuration of a game.

    This class defines the settings that determine how a game is structured, including the number of colors, dots, allowed attempts, and game mode.

    Attributes:
        number_of_colors (int): The number of colors a dot can be.
        number_of_dots (int): The number of dots in a code.
        attempts_allowed (int): The maximum number of attempts allowed for the code cracker to guess the code.
        game_mode (GameMode): The game mode determine who is Player 1 and Player 2.
    """

    number_of_colors: int
    number_of_dots: int
    attempts_allowed: int
    game_mode: GameMode
