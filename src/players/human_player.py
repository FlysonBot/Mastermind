from getpass import getpass
from typing import Optional, Union

from src.players.abstract_player import CodeCracker, CodeSetter
from src.utils import get_feedback
from src.validation import ValidGuess


class HumanSetter(CodeSetter):
    """A class to represent a human code setter."""

    def set_secret_code(self) -> Optional[str]:
        """
        Sets the secret code for the game.
        Return 'd' if player discarded the game. Otherwise doesn't return anything.
        """
        valid_guess = ValidGuess(
            [1] * self.GAME.number_of_dots,
            number_of_dots=self.GAME.number_of_dots,
            number_of_colors=self.GAME.number_of_colors,
        )
        while True:
            secret = getpass("Enter the secret code: ")
            if secret == "?":
                hint = f"""
                Enter a {self.GAME.number_of_dots}-digit number with digit ranging from 1 to {self.GAME.number_of_colors}.
                For example, a 6-digit 4-color code can be 123412, or 1,2,3,4,1,2
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                """
                print(hint)
                continue
            if secret == "d":
                print("Game discarded.")
                return "d"

            try:
                valid_guess.value = valid_guess.validate(secret)
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")
            else:  # Confirm password
                confirm = getpass("Confirm the secret code: ")
                if confirm != secret:
                    print("Code does not match. Try again.")
                    continue
                self.SECRET_CODE = valid_guess
                return

    def get_feedback(self, guess: tuple) -> tuple:
        """Obtains feedback for a given guess."""
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")
        return get_feedback(guess, self.SECRET_CODE, self.GAME.number_of_colors)


class HumanCracker(CodeCracker):
    """A class to represent a human code cracker."""

    def __init__(self, game: "Game") -> None:  # type: ignore
        """Initializes the human code cracker."""
        win_message = "Congratulations! You won in {step} steps!"
        lose_message = "Sorry, you lost. The secret code was {step}."
        super().__init__(game, win_message, lose_message)

    def obtain_guess(self) -> Union[tuple, str]:
        """
        Obtains a guess from the player.
        Could return the guess as tuple or command (d,q,u,r) as string.
        """
        valid_guess = ValidGuess(
            [1] * self.GAME.number_of_dots,
            number_of_dots=self.GAME.number_of_dots,
            number_of_colors=self.GAME.number_of_colors,
        )
        while True:
            guess = input("Enter your guess: ")
            if guess == "?":
                hint = f"""
                Enter a {self.GAME.number_of_dots}-digit number with digit ranging from 1 to {self.GAME.number_of_colors}.
                For example, a 6-digit 4-color code can be 123412, or 1,2,3,4,1,2
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                (q) to save and quit
                (u) to undo
                (r) to redo
                """
                print(hint)
                continue
            if guess == "d":
                print("Game discarded.")
                return "d"
            if guess == "q":  # quit
                print("Game saved.")
                return "q"
            if guess == "u":  # undo
                return "u"
            if guess == "r":  # redo
                return "r"

            try:
                valid_guess.value = valid_guess.validate(guess)
                return valid_guess.value
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")
            except valid_guess.ValidationError:
                print(
                    f"Guess must consist of {self.GAME.number_of_dots} integers in range [1, {self.GAME.number_of_colors}]"
                )
                print("To get more help, enter '?'")
