from typing import Optional

from src.game.game_flow import GameFlow
from src.game.game_parameter import GameParameter
from src.game.player_logic import PlayerLogic


class Game:
    """
    The main entry point for the Mastermind game.

    Args:
        number_of_colors (int): The number of colors in the game.
        number_of_dots (int): The number of dots in each combination.
        maximum_attempts (int): The maximum number of attempts allowed in the game.
        game_mode (str): The game mode, such as "HvH", "HvAI", "AIvH", or "AIvAI".
    """

    def __init__(self, number_of_colors, number_of_dots, maximum_attempts, game_mode):
        self._state = GameParameter(
            number_of_colors, number_of_dots, maximum_attempts, game_mode
        )
        self._board = self._state._board
        self._player_logic = PlayerLogic(self._state)
        self._game_flow = GameFlow(self._state, self._player_logic)

    def start_game(self) -> Optional[str]:
        """
        Starts the game.

        Returns:
            Optional[str]: A command from the player, if any.
        """
        return self._game_flow.start_game()

    def resume_game(self) -> Optional[str]:
        """
        Resumes the game.

        Returns:
            Optional[str]: A command from the player, if any.
        """
        return self._game_flow.resume_game()

    def __len__(self) -> int:
        """
        Returns the number of attempts made in the game.
        """
        return len(self._board)

    @property
    def number_of_colors(self) -> int:
        """
        Returns the number of colors in the game.
        """
        return self._state.number_of_colors
    
    @property
    def number_of_dots(self) -> int:
        """
        Returns the number of dots in each combination.
        """
        return self._state.number_of_dots
    
    @property
    def maximum_attempts(self) -> int:
        """
        Returns the maximum number of attempts allowed in the game.
        """
        return self._state.MAXIMUM_ATTEMPTS
    
    @property
    def game_mode(self) -> str:
        """
        Returns the game mode.
        """
        return self._state.GAME_MODE
