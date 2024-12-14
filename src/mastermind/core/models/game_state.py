from dataclasses import dataclass
from typing import Optional

from mastermind.core.controllers.players import Player


@dataclass
class GameState:
    """
    Dataclass for maintaining the current state of the game, indicating whether the game has started, if it is over, and who won.

    Attributes:
        game_started (bool): A flag indicating if the game has started.
        game_over (bool): A flag indicating if the game has ended.
        winner (Player): The player who won the game, if any. Only top level player (CodeSetter or Codebreaker) is allowed.
    """

    game_started: bool = False
    game_over: bool = False
    winner: Optional[Player] = None
