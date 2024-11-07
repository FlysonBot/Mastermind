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

    @abstractmethod
    def win_message(self) -> None:
        """
        Prints a message when the player wins.
        """
        pass

    @abstractmethod
    def lose_message(self) -> None:
        """
        Prints a message when the player loses.
        """
        pass


class HumanCracker(Player):
    """
    A class to represent a human cracker.
    """
    pass


class HumanSetter(Player):
    """
    A class to represent a human setter.
    """
    pass


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