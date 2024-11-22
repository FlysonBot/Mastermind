"""
This module defines the Game class, which initializes the game state, player logic, and game flow, and provides methods to start and resume the game.

Each instance of Game represents a single game in Mastermind.
"""

from typing import Optional

from src.game.game_flow import GameFlow
from src.game.game_state import GameParameter
from src.game.player_logic import PlayerLogic


class Game:
    """
    Represents the main game object for a Mastermind-like game.

    The Game class initializes the game state, player logic, and game flow, and provides methods to start and resume the game.

    Args:
        number_of_colors (int): The number of colors available in the game.
        number_of_dots (int): The number of dots (or pegs) in each guess.
        maximum_attempts (int): The maximum number of attempts allowed in the game.
        game_mode (str): The game mode, which can be "HvH", "HvAI", "AIvH", or "AIvAI".
    """

    def __init__(self, number_of_colors, number_of_dots, maximum_attempts, game_mode):
        self._state = GameParameter(
            number_of_colors, number_of_dots, maximum_attempts, game_mode
        )
        self._board = self._state._board
        self._player_logic = PlayerLogic(self)
        self._game_flow = GameFlow(self._state, self._player_logic)

    def start_game(self) -> Optional[str]:
        """
        Starts a new game.

        Returns:
            Optional[str]: A command from the user (e.g., "q" for quit, "d" for discard) if the game is terminated.
        """

        return self._game_flow.start_game()

    def resume_game(self) -> Optional[str]:
        """
        Resumes a previously started game.

        Returns:
            Optional[str]: A command from the user (e.g., "q" for quit, "d" for discard) if the game is terminated.
        """

        return self._game_flow.resume_game()
