from typing import Tuple

from src.utils import Stack
from src.validation import BaseModel, ValidFeedback, ValidGuess


class GameBoard(BaseModel):
    """
    A class to represent a Mastermind game board, storing guesses and feedback.

    This class manages the state of the game board, including adding guesses, retrieving the last guess and feedback, and handling the number of guesses made.

    Args:
        number_of_colors (int): The number of colors available for guesses.
        number_of_dots (int): The number of dots in each guess.

    Raises:
        EmptyBoardError: If an operation is attempted on an empty board.

    Examples:
        board = _Board(number_of_colors=6, number_of_dots=4)
        board.add_guess((1, 2, 3, 4), (1, 0))
        last_guess = board.last_guess()
    """

    class EmptyBoardError(Exception):
        """Custom exception for empty board."""

        pass

    def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
        """Initializes the board."""
        self.NUMBER_OF_COLORS = number_of_colors
        self.NUMBER_OF_DOTS = number_of_dots

        self._number_of_guesses_made = 0
        self._guesses = Stack()
        self._feedbacks = Stack()

    def __len__(self) -> int:
        """Returns the number of guesses made."""
        return self._number_of_guesses_made

    def __getitem__(self, index: int) -> Tuple:
        """Returns the guess and feedback at the given index."""
        return self._guesses[index], self._feedbacks[index]

    def last_guess(self) -> Tuple:
        """Returns the last guess."""
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._guesses.top()

    def last_feedback(self) -> Tuple:
        """Returns the last feedback."""
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._feedbacks.top()

    def remove_last(self) -> Tuple:
        """Undoes the last guess and its feedback."""
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to remove.")

        self._number_of_guesses_made -= 1

        return self._guesses.pop(), self._feedbacks.pop()

    def add_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """Adds a guess and its feedback to the board."""
        ValidGuess(
            guess,
            number_of_dots=self.NUMBER_OF_DOTS,
            number_of_colors=self.NUMBER_OF_COLORS,
        )

        ValidFeedback(feedback, number_of_dots=self.NUMBER_OF_DOTS)

        self._guesses.push(guess)
        self._feedbacks.push(feedback)
        self._number_of_guesses_made += 1

    def clear(self) -> None:
        """Clears the board."""
        self._guesses.clear()
        self._feedbacks.clear()
        self._number_of_guesses_made = 0
