from typing import Tuple

from src.utils import Stack
from src.validation import ValidatedClass, ValidFeedback, ValidCombination


class GameBoard(ValidatedClass):
    """
    Represents the game board for a Mastermind game.

    The GameBoard class manages the game's guesses and feedbacks, allowing players to make guesses, retrieve past guesses and feedbacks, and clear the board.

    Attributes:
        NUMBER_OF_COLORS (int): The number of colors available in the game.
        NUMBER_OF_DOTS (int): The number of dots (or pegs) in each guess.
        _number_of_guesses_made (int): The number of guesses made so far.
        _guesses (Stack): A stack of the guesses made so far.
        _feedbacks (Stack): A stack of the feedbacks received for the guesses made so far.

    Raises:
        EmptyBoardError: If there are no guesses to retrieve or remove.
    """

    class EmptyBoardError(Exception):
        """
        Exception raised when trying to access the game board when it is empty.
        """

        pass

    def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
        self.NUMBER_OF_COLORS = number_of_colors
        self.NUMBER_OF_DOTS = number_of_dots

        self._number_of_guesses_made = 0
        self._guesses = Stack()
        self._feedbacks = Stack()

    def __len__(self) -> int:
        """
        Returns the number of guesses made on the game board.
        """
        return self._number_of_guesses_made

    def __getitem__(self, index: int) -> Tuple:
        """
        Returns the guess and feedback at the specified index.
        """
        return self._guesses[index], self._feedbacks[index]

    def last_guess(self) -> Tuple:
        """
        Returns the last guess made on the game board.

        Returns:
            Tuple: A tuple representation of the last guess.

        Raises:
            EmptyBoardError: If there are no guesses on the game board.
        """
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._guesses.top()

    def last_feedback(self) -> Tuple:
        """
        Returns the feedback for the last guess made on the game board.

        Returns:
            Tuple: A tuple representation of the last feedback.

        Raises:
            EmptyBoardError: If there are no guesses on the game board.
        """
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._feedbacks.top()

    def remove_last(self) -> Tuple:
        """
        Removes the last guess and feedback from the game board.

        Returns:
            Tuple: The removed guess and feedback.

        Raises:
            EmptyBoardError: If there are no guesses on the game board.
        """
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to remove.")

        self._number_of_guesses_made -= 1

        return self._guesses.pop(), self._feedbacks.pop()

    def add_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
        """
        Adds a new guess and its corresponding feedback to the game board.

        Args:
            guess (Tuple[int, ...]): The new guess.
            feedback (Tuple[int, ...]): The feedback for the new guess.
        """
        ValidCombination(
            guess,
            number_of_dots=self.NUMBER_OF_DOTS,
            number_of_colors=self.NUMBER_OF_COLORS,
        )

        ValidFeedback(feedback, number_of_dots=self.NUMBER_OF_DOTS)

        self._guesses.push(guess)
        self._feedbacks.push(feedback)
        self._number_of_guesses_made += 1

    def clear(self) -> None:
        """
        Clears the game board, removing all guesses and feedbacks.
        """
        self._guesses.clear()
        self._feedbacks.clear()
        self._number_of_guesses_made = 0
