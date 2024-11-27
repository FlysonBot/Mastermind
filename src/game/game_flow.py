from typing import Optional

from src.game.game_parameter import GameParameter
from src.game.player_logic import PlayerLogic


class GameFlow:
    """
    Manages the flow of the Mastermind game.

    Args:
        game_state (GameState): The state of the game.
        player_logic (PlayerLogic): The logic for the players.
    """

    def __init__(self, game_state: GameParameter, player_logic: PlayerLogic) -> None:
        self.game_state = game_state
        self.player_logic = player_logic

    def start_game(self) -> Optional[str]:
        """
        Starts the game.

        Returns:
            Optional[str]: A command from the player, if any.
        """
        if self.game_state.game_started:
            raise NotImplementedError("Game has already started.")

        self.game_state.game_started = True
        self.player_logic.initialize_players()
        if self.player_logic.PLAYER_SETTER.set_secret_code() == "d":
            return "d"  # code setter discarded the game

        return self._play_game()

    def resume_game(self) -> Optional[str]:
        """
        Resumes the game.

        Returns:
            Optional[str]: A command from the player, if any.
        """
        if not self.game_state.game_started:
            raise NotImplementedError("Game has not started yet.")

        return self._play_game()

    def _play_game(self) -> Optional[str]:
        """
        Plays the game and retrieves a command from the player, if any.

        Returns:
            Optional[str]: A command from the player, if any.
        """

        command = self.player_logic.process_player_guessing()

        self.output_result()
        return command

    def output_result(self) -> None:
        """
        Outputs the result of the game.
        """
        self.game_state.check_and_update_win_status()

        if self.game_state.win_status is None:
            return

        if self.game_state.win_status:
            self.player_logic.PLAYER_CRACKER.win_message()

        else:
            self.player_logic.PLAYER_CRACKER.lose_message()
