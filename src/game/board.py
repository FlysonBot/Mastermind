from typing import Tuple

from src.utils import Stack
from src.validation import BaseModel, ValidFeedback, ValidGuess


class GameBoard(BaseModel):
    class EmptyBoardError(Exception):
        pass

    def __init__(self, number_of_colors: int, number_of_dots: int) -> None:
        self.NUMBER_OF_COLORS = number_of_colors
        self.NUMBER_OF_DOTS = number_of_dots

        self._number_of_guesses_made = 0
        self._guesses = Stack()
        self._feedbacks = Stack()

    def __len__(self) -> int:
        return self._number_of_guesses_made

    def __getitem__(self, index: int) -> Tuple:
        return self._guesses[index], self._feedbacks[index]

    def last_guess(self) -> Tuple:
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._guesses.top()

    def last_feedback(self) -> Tuple:
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to return.")

        return self._feedbacks.top()

    def remove_last(self) -> Tuple:
        if self._number_of_guesses_made == 0:
            raise self.EmptyBoardError("No guesses to remove.")

        self._number_of_guesses_made -= 1

        return self._guesses.pop(), self._feedbacks.pop()

    def add_guess(self, guess: Tuple[int, ...], feedback: Tuple[int, ...]) -> None:
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
        self._guesses.clear()
        self._feedbacks.clear()
        self._number_of_guesses_made = 0
