from dataclasses import dataclass

from mastermind.core.models.data.game_mode import GameMode


@dataclass
class GameConfiguration:
    """Dataclass for the configuration of a game."""

    number_of_colors: int
    number_of_positions: int
    attempts_allowed: int
    game_mode: GameMode
