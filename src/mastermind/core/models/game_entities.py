from dataclasses import dataclass

from mastermind.core.controllers.players import Player


@dataclass
class GameEntities:
    """
    Dataclass for the entities of a game (such as players or those from plugins).

    This class represents the key participants in a game, specifically the players involved in setting and breaking the code. It serves as a structured way to manage and reference these entities throughout the game's lifecycle.

    Attributes:
        code_setter (Player): The player responsible for setting the code.
        code_breaker (Player): The player tasked with breaking the code.
    """

    code_setter: Player
    code_breaker: Player
