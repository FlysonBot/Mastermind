from typing import Optional

from src.game.board import GameBoard
from src.validation import TrueFuse


class GameParameter:
    """
    Represents the current state of the Mastermind-like game.

    The GameState class manages the game board, the game mode, the maximum number of attempts, and the win status.

    Args:
        number_of_colors (int): The number of colors available in the game.
        number_of_dots (int): The number of dots (or pegs) in each guess.
        maximum_attempts (int): The maximum number of attempts allowed in the game.
        game_mode (str): The game mode, which can be "HvH", "HvAI", "AIvH", or "AIvAI".
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

        self._board = GameBoard(number_of_colors, number_of_dots)
        self._game_started = TrueFuse(False)
        self._win_status = None

    def check_and_update_win_status(self) -> bool | None:
        """
        Checks the current state of the game and updates the win status.

        Returns:
            bool | None: The updated win status (True if the player has won, False if the player has lost, or None if the game is still in progress).
        """

        if self._last_guess_is_secret(self):
            self._win_status = True

        elif self._last_feedback_is_perfect(self):
            self._win_status = True

        elif self._reached_maximum_attempts(self):
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

    @property
    def game_started(self) -> bool:
        return self._game_started

    def __len__(self) -> int:
        return len(self._board)

    def _last_guess_is_secret(self) -> bool:
        return (
            hasattr(self, "SECRET_CODE")
            and self._board.last_guess() == self.SECRET_CODE
        )

    def _last_feedback_is_perfect(self) -> bool:
        return self._board.last_feedback() == (self.number_of_dots, 0)

    def _reached_maximum_attempts(self) -> bool:
        return len(self._board) == self.MAXIMUM_ATTEMPTS
