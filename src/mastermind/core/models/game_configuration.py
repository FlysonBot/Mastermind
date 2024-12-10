from dataclasses import dataclass

from mastermind.core.models.game_mode import GameMode


@dataclass(frozen=True)
class GameConfiguration:
    """
    Dataclass for the configuration of a game.

    This class defines the settings that determine how a game is structured, including the number of colors, dots, allowed attempts, and game mode.

    Attributes:
        NUMBER_OF_COLORS (int): The number of colors a dot can be.
        NUMBER_OF_DOTS (int): The number of dots in a code.
        ATTEMPTS_ALLOWED (int): The maximum number of attempts allowed for the code  to guess the code.
        GAME_MODE (GameMode): The game mode determine who is Player 1 and Player 2.
    """

    NUMBER_OF_COLORS: int
    NUMBER_OF_DOTS: int
    ATTEMPTS_ALLOWED: int
    GAME_MODE: GameMode

    def __str__(self):
        return f"{self.NUMBER_OF_COLORS}x{self.NUMBER_OF_DOTS}, {self.ATTEMPTS_ALLOWED} attempts in {self.GAME_MODE} mode"
