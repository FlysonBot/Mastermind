from random import randint

from src.players.abstract_player import CodeCracker, CodeSetter
from src.utils import generate_feedback


class AICodeSetter(CodeSetter):
    def set_secret_code(self) -> None:
        # Generate random code
        self.SECRET_CODE = tuple(
            randint(1, self.GAME.number_of_colors)
            for _ in range(self.GAME.number_of_dots)
        )

    def get_feedback(self, guess: tuple) -> tuple:
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")
        return generate_feedback(guess, self.SECRET_CODE, self.GAME.number_of_colors)


class AICodeCracker(CodeCracker):
    def __init__(self, game: "Game") -> None:  # type: ignore  # noqa: F821
        win_message = "Congratulations! You won in {step} steps!"
        lose_message = "Sorry, you lost. The secret code was {step}."
        super().__init__(game, win_message, lose_message)

    def obtain_guess(self) -> tuple:
        # TODO: Implement AI solver logic to generate guess.
        pass
