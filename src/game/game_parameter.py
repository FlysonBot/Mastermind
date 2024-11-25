from typing import Optional

from src.game.board import GameBoard
from src.validation import TrueFuse, ValidatedClass


class GameParameter(ValidatedClass):
    """
    Represents the state of the Mastermind game.

    Args:
        number_of_colors (int): The number of colors in the game.
        number_of_dots (int): The number of dots in each combination.
        maximum_attempts (int): The maximum number of attempts allowed in the game.
        game_mode (str): The game mode, such as "HvH", "HvAI", "AIvH", or "AIvAI".
    """

    def __init__(
        self,
        number_of_colors: int,
        number_of_dots: int,
        maximum_attempts: int,
        game_mode: str,
    ) -> None:
        self.MAXIMUM_ATTEMPTS = maximum_attempts
        self.GAME_MODE = game_mode
        self.game_started = TrueFuse(False)  # validation enforced by ValidatedClass

        self._board = GameBoard(number_of_colors, number_of_dots)
        self._win_status = None

    def check_and_update_win_status(self) -> bool | None:
        """
        Checks the game state and updates the win status.

        Returns:
            bool | None: The win status, or None if the game is still in progress.
        """

        if len(self) == 0:
            self._win_status = None
            return self._win_status

        if self._last_guess_is_secret() or self._last_feedback_is_perfect():
            self._win_status = True

        elif self._reached_maximum_attempts():
            self._win_status = False

        else:
            self._win_status = None

        return self._win_status

    @property
    def number_of_colors(self) -> int:
        return self._board.NUMBER_OF_COLORS

    @property
    def number_of_dots(self) -> int:
        return self._board.NUMBER_OF_DOTS

    @property
    def win_status(self) -> Optional[bool]:
        return self._win_status

    def __len__(self) -> int:
        return len(self._board)

    def _last_guess_is_secret(self) -> bool:
        """
        Checks if the last guess made on the game board matches the secret code.
        """
        return (
            hasattr(self, "SECRET_CODE")
            and self._board.last_guess() == self.SECRET_CODE
        )

    def _last_feedback_is_perfect(self) -> bool:
        """
        Checks if the feedback for the last guess is perfect (all dots in the correct position).
        """
        return self._board.last_feedback() == (self.number_of_dots, 0)

    def _reached_maximum_attempts(self) -> bool:
        """
        Checks if the maximum number of attempts has been reached.
        """
        return len(self._board) == self.MAXIMUM_ATTEMPTS
