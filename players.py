# players.py
from .validation import BaseModel
from abc import ABC, abstractmethod


# Abstract Class for Player Unit
class Player(ABC, BaseModel):
    """
    A class to represent a player.
    """

    def __init__(self, game: Game) -> None:
        """
        Initializes the player.
        """
        self.GAME = game

    @abstractmethod
    def obtain_guess(self) -> tuple:
        """
        Obtains a guess from the player.
        """
        raise NotImplementedError("This method must be implemented in a subclass.")


class CodeSetter(Player):
    """
    A class to represent a code setter.
    """
    pass


class CodeCracker(Player):
    """
    A class to represent a code cracker.
    """
    pass