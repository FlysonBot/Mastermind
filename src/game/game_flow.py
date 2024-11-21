from typing import Optional

from src.game.game_state import GameState
from src.game.player_logic import PlayerLogic


class GameFlow:
    def __init__(self, game_state: GameState, player_logic: PlayerLogic) -> None:
        self.game_state = game_state
        self.player_logic = player_logic

    def start_game(self) -> Optional[str]:  # sourcery skip: class-extract-method
        """Starts the game."""
        # Check Condition
        if self._game_started:
            raise NotImplementedError("Game has already started.")

        # Start Game
        self._game_started = True
        self.initialize_players()
        self.PLAYER_SETTER.set_secret_code()

        return self._play_game()

    def resume_game(self) -> Optional[str]:
        """Resumes the game."""
        # Check Condition
        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")

        return self._play_game()

    def _play_game(self) -> Optional[str]:
        # Play game and retrieve user command if any
        command = self.player_logic.process_player_guessing()

        # After game is terminated
        self.game_state.output_result(self.player_logic.PLAYER_CRACKER)
        return command
