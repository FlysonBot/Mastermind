from typing import Optional

from src.game.game_state import GameState
from src.game.player_logic import PlayerLogic


class GameFlow:
    def __init__(self, game_state: GameState, player_logic: PlayerLogic) -> None:
        self.game_state = game_state
        self.player_logic = player_logic

    def start_game(self) -> Optional[str]:  # sourcery skip: class-extract-method
        if self._game_started:
            raise NotImplementedError("Game has already started.")

        self._game_started = True
        self.initialize_players()
        self.PLAYER_SETTER.set_secret_code()

        return self._play_game()

    def resume_game(self) -> Optional[str]:
        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")

        return self._play_game()

    def _play_game(self) -> Optional[str]:
        # Play game and retrieve user command if any
        command = self.player_logic.process_player_guessing()

        # After game is terminated
        self.output_result()
        return command

    def output_result(self) -> None:
        self.game_state.check_and_update_win_status()

        if self.win_status is None:
            return

        if self.win_status:
            self.player_logic.PLAYER_CRACKER.win_message()

        else:
            self.player_logic.PLAYER_CRACKER.lose_message()
