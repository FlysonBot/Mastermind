from getpass import getpass
from typing import Optional, Union

from mastermind.players.abstract_player import CodeCracker, CodeSetter
from mastermind.utils import generate_feedback
from mastermind.validation import ValidCombination
from mastermind.validation.base.exceptions import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)


class HumanCodeSetter(CodeSetter):
    def set_secret_code(self) -> Optional[str]:
        valid_guess = ValidCombination(
            number_of_dots=self.game_state.number_of_dots,
            number_of_colors=self.game_state.number_of_colors,
        )

        while True:
            secret = getpass("Enter the secret code: ")

            if secret == "?":
                hint = f"""
                Enter a {self.game_state.number_of_dots}-digit number with digit ranging from 1 to {self.game_state.number_of_colors}.
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
                valid_guess.validate_value(secret)

            except (TypeValidationError, InputConversionError) as e:
                print(e)
                print("To get more help, enter '?'")

            except RangeError:
                print(
                    f"Guess must consist of {self.game_state.number_of_dots} integers in range [1, {self.game_state.number_of_colors}]"
                )
                print("To get more help, enter '?'")

            else:  # Confirm password
                confirm = getpass("Confirm the secret code: ")

                if confirm != secret:
                    print("Code does not match. Try again.")
                    continue

                self.SECRET_CODE = valid_guess.validate_value(secret)
                return

    def get_feedback(self, guess: tuple) -> tuple:
        if not hasattr(self, "SECRET_CODE"):
            raise NotImplementedError("Secret code not set yet.")

        return generate_feedback(
            guess, self.SECRET_CODE, self.game_state.number_of_colors
        )


class HumanCodeCracker(CodeCracker):
    def __init__(self, player_logic: "PlayerLogic") -> None:  # type: ignore  # noqa: F821
        win_message = "Congratulations! You won in {step} steps!"
        lose_message = "Sorry, you lost. The secret code was {step}."
        super().__init__(player_logic, win_message, lose_message)

    def obtain_guess(self) -> Union[tuple, str]:
        valid_guess = ValidCombination(
            number_of_dots=self.game_state.number_of_dots,
            number_of_colors=self.game_state.number_of_colors,
        )

        while True:
            guess = input("Enter your guess: ")

            if guess == "?":
                hint = f"""
                Enter a {self.game_state.number_of_dots}-digit number with digit ranging from 1 to {self.game_state.number_of_colors}.
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
                return valid_guess.validate_value(guess)

            except (TypeValidationError, InputConversionError) as e:
                print(e)
                print("To get more help, enter '?'")

            except RangeError:
                print(
                    f"Guess must consist of {self.game_state.number_of_dots} integers in range [1, {self.game_state.number_of_colors}]"
                )
                print("To get more help, enter '?'")
