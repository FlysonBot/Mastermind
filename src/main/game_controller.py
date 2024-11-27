from typing import Any

from src.game.game import Game
from src.main.game_history import GameHistoryManager
from src.storage.user_data import UserDataManager
from src.validation.base.base import Validator
from src.validation.models.numeric import MaximumAttempts, NumberOfColors, NumberOfDots


class GameController:
    """Communication between MainUI and the gameboard."""

    @classmethod
    def validate_input(cls, prompt: str, validator: Validator) -> Any:
        """Get user input and validate it."""
        while True:
            try:
                user_input = input("\n" + prompt)
                if validator(user_input):
                    return user_input
                else:
                    print("Invalid input. Please try again.")

            except Exception as e:
                print(f"Invalid input. {e}")

    @classmethod
    def get_game_parameters(cls) -> tuple[int, int, int]:
        """Get the number of colors, number of dots, and number of rounds from user."""
        num_of_colors = cls.validate_input(
            "Enter the number of colors (2-10): ", NumberOfColors
        )
        num_of_dots = cls.validate_input(
            "Enter the number of dots (2-10): ", NumberOfDots
        )
        max_attempts = cls.validate_input(
            "Enter the maximum number of attempts: ", MaximumAttempts
        )
        return num_of_colors, num_of_dots, max_attempts

    @classmethod
    def start_new_game(cls, game_mode: str) -> None:
        """Start a new game."""
        if game_mode not in ["HvH", "HvAI", "AIvH", "AIvAI"]:
            raise AssertionError("Unexpected invalid game mode.")

        parameters = cls.get_game_parameters()  # get user input
        game = Game(*parameters, game_mode)  # create a new game
        game.start_game()  # start the game
        GameHistoryManager.save_game(game)  # save the game

    @classmethod
    def resume_game(cls, game_index: int) -> None:
        """Resume a saved game."""
        # Retrieve game
        game = UserDataManager().saved_games[game_index]["game"]

        # Resume game
        game.resume_game()

        # Update saved games
        UserDataManager().saved_games[game_index] = (
            GameHistoryManager().generate_meta_data(game)
        )
