from typing import Optional

from src.game.board import GameBoard
from src.players.abstract_player import CodeCracker
from src.validation import TrueFuse


class GameState:
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

    def check_and_update_win_status(self) -> Optional[bool]:
        if len(self._board) == 0:
            self._win_status = None

        if self._last_guess_is_secret(self):
            self._win_status = True

        elif self._last_feedback_is_perfect(self):
            self._win_status = True

        elif self._reached_maximum_attempts(self):
            self._win_status = False

        # When non of the above is true, game continues
        return self._win_status

    def output_result(self, PLAYER_CRACKER: CodeCracker) -> None:
        self.check_and_update_win_status()

        if self.win_status is None:
            return

        if self.win_status:
            PLAYER_CRACKER.win_message()

        else:
            PLAYER_CRACKER.lose_message()

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
