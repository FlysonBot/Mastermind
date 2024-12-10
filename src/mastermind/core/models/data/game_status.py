from dataclasses import dataclass


@dataclass
class GameStatus:
    """Dataclass for the status of a game."""

    game_started: bool
    game_over: bool
    game_won: bool
