from typing import Optional

from src.game.game_flow import GameFlow
from src.game.game_state import GameState
from src.game.player_logic import PlayerLogic


class Game:
    def __init__(self, number_of_colors, number_of_dots, maximum_attempts, game_mode):
        self._state = GameState(
            number_of_colors, number_of_dots, maximum_attempts, game_mode
        )
        self._board = self._state._board
        self._player_logic = PlayerLogic(self)
        self._game_flow = GameFlow(self._state, self._player_logic)

    def start_game(self) -> Optional[str]:
        return self._game_flow.start_game()

    def resume_game(self) -> Optional[str]:
        return self._game_flow.resume_game()
