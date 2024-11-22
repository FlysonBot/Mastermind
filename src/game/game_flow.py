from typing import Optional

from src.game.game_state import GameParameter
from src.game.player_logic import PlayerLogic


class GameFlow:
    """
    Manages the flow of the Mastermind-like game.

    The GameFlow class is responsible for starting and resuming the game, as well as handling the game loop and outputting the final result.

    Args:
        game_state (GameState): The current state of the game.
        player_logic (PlayerLogic): The logic for the players in the game.
    """

    def __init__(self, game_state: GameParameter, player_logic: PlayerLogic) -> None:
        self.game_state = game_state
        self.player_logic = player_logic

    def start_game(self) -> Optional[str]:
        """
        Starts a new game.

        Returns:
            Optional[str]: A command from the user (e.g., "q" for quit, "d" for discard) if the game is terminated.
        """

        if self._game_started:
            raise NotImplementedError("Game has already started.")

        self._game_started = True
        self.initialize_players()
        self.PLAYER_SETTER.set_secret_code()

        return self._play_game()

    def resume_game(self) -> Optional[str]:
        """
        Resumes a previously started game.

        Returns:
            Optional[str]: A command from the user (e.g., "q" for quit, "d" for discard) if the game is terminated.
        """

        if not self._game_started:
            raise NotImplementedError("Game has not started yet.")

        return self._play_game()

    def _play_game(self) -> Optional[str]:
        """
        Plays the game and retrieves any user command.

        Returns:
            Optional[str]: A command from the user (e.g., "q" for quit, "d" for discard) if the game is terminated.
        """

        command = self.player_logic.process_player_guessing()

        self.output_result()
        return command

    def output_result(self) -> None:
        """Outputs the result of the game, including the win/loss status."""

        self.game_state.check_and_update_win_status()

        if self.win_status is None:
            return

        if self.win_status:
            self.player_logic.PLAYER_CRACKER.win_message()

        else:
            self.player_logic.PLAYER_CRACKER.lose_message()
