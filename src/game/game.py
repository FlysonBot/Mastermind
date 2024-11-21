from typing import Optional

from src.game.board import GameBoard
from src.game.game_flow import GameFlow
from src.game.game_state import GameState
from src.game.player_logic import PlayerLogic


class Game:
    def __init__(self, number_of_colors, number_of_dots, maximum_attempts, game_mode):
        self._board = GameBoard(number_of_colors, number_of_dots)
        self._state = GameState(self._board, maximum_attempts)
        self._player_logic = PlayerLogic(self)
        self._game_flow = GameFlow(self._state, self._player_logic)

    def start_game(self) -> Optional[str]:
        return self._game_flow.start_game()

    def resume_game(self) -> Optional[str]:
        return self._game_flow.resume_game()
