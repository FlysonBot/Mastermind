from dataclasses import dataclass

from mastermind.core.controllers.players import Player


@dataclass(frozen=True)
class GameEntities:
    """
    Dataclass for the entities of a game (such as players or those from plugins).

    This class represents the key participants in a game, specifically the players involved in setting and breaking the code. It serves as a structured way to manage and reference these entities throughout the game's lifecycle.

    Attributes:
        CODE_SETTER (Player): The player responsible for setting the code.
        CODE_BREAKER (Player): The player tasked with breaking the code.
    """

    CODE_SETTER: Player
    CODE_BREAKER: Player

    def __str__(self):
        return f"Code Setter: {self.CODE_SETTER.__qualname__}, Code Breaker: {self.CODE_BREAKER.__qualname__}"
