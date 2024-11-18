from random import randint

from mastermind.players.abstract_player import CodeCracker, CodeSetter
from mastermind.utils import get_feedback


class AISetter(CodeSetter):
    """A class to represent an AI code setter."""

    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        # Generate random code
        number_of_colors = self.GAME.number_of_colors
        number_of_dots = self.GAME.number_of_dots
        self.SECRET_CODE = tuple(
            randint(1, number_of_colors) for _ in range(number_of_dots)
        )

    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")
        return get_feedback(guess, self.SECRET_CODE, self.GAME.number_of_colors)


class AICracker(CodeCracker):
    """A class to represent an AI code cracker."""

    pass  # TODO: Implement solver logic.
