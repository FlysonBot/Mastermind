from abc import ABC, abstractmethod

from src.utils import FStringTemplate, Stack
from src.validation import BaseModel


class Player(ABC, BaseModel):
    """An abstract class to represent a player."""

    def __init__(self, game: "Game") -> None:  # type: ignore
        """Initializes the player."""
        self.GAME = game
        self.undo_stack = Stack()  # For undo and redo functionality

    @abstractmethod
    def undo(self, item: tuple) -> None:
        """Push the item to the undo stack."""
        if len(self.GAME._board) == 0:
            raise self.GAME._board.EmptyBoardError("Cannot undo from empty board.")
        self.undo_stack.push(
            item
        )  # item can be guess or feedback, varies by player type

    def redo(self) -> None:
        """Pop and return the last guess from undo stack."""
        if len(self.undo_stack) == 0:
            raise IndexError("Cannot undo from empty board.")
        return self.undo_stack.pop()

    def clear_undo(self) -> None:
        """Clear the undo stack."""
        self.undo_stack.clear()


class CodeSetter(Player):
    """An abstract class to represent a code setter."""

    @abstractmethod
    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        pass

    @abstractmethod
    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        pass

    def undo(self) -> None:
        """Update the undo stack with last feedback."""
        super().undo(self.GAME._board.last_feedback())


class CodeCracker(Player):
    """An abstract class to represent a code cracker."""

    def __init__(self, game: "Game", win_msg: str, lose_msg: str) -> None:  # type: ignore
        """Initializes the code cracker."""
        super().__init__(game)
        self._win_message = FStringTemplate(win_msg)
        self._lose_message = FStringTemplate(lose_msg)

    def win_message(self) -> None:
        """Prints a message when the game is won."""
        print(self._win_message.eval(step=len(self.GAME)))

    def lose_message(self) -> None:
        """Prints a message when the game is lost."""
        print(self._lose_message.eval(step=len(self.GAME)))

    @abstractmethod
    def obtain_guess(self) -> tuple:
        """Obtains a guess from the player."""
        pass

    def undo(self) -> None:
        """Update the undo stack with last guess"""
        super().undo(self.GAME._board.last_guess())
