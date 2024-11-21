from typing import Union

from src.players.abstract_player import CodeSetter
from src.validation import ValidFeedback


class ExternalCodeSetter(CodeSetter):
    """A class to represent an external code setter."""

    def set_secret_code(self) -> None:
        """Sets the secret code for the game."""
        pass  # There is no code available for external game, skip it

    def get_feedback(self, guess: tuple) -> Union[tuple, str]:
        """
        Obtains external feedback from the user.
        Could return the feedback as tuple or command (d,q,u) as string.
        """
        valid_feedback = ValidFeedback((0, 0), number_of_dots=self.GAME.number_of_dots)
        while True:
            feedback = input("Enter the feedback: ")
            if feedback == "?":
                hint = f"""
                Enter a 2 digit number (optionally separated by comma) between 0 and {self.GAME.number_of_dots}.
                The first digit represents the number of black pegs, the second represents the number of white pegs.
                For example: 01 or 0,1 -> (0, 1) -> 0 black pegs, 1 white peg.
                Or, you can enter a command:
                (?) for help
                (d) to discard the game
                (q) to save and quit
                (u) to undo
                """
                print(hint)
                continue
            if feedback == "d":
                print("Game discarded.")
                return "d"
            if feedback == "q":  # quit
                print("Game saved.")
                return "q"
            if feedback == "u":  # undo
                return "u"

            try:
                valid_feedback.value = valid_feedback.validate_value(feedback)
                return valid_feedback.value
            except ValueError as e:
                print(e)
                print("To get more help, enter '?'")
            except valid_feedback.ValidationError:
                print(
                    f"Feedback must consist of 2 integer in range [0, {self.GAME.number_of_dots})"
                )
                print("To get more help, enter '?'")
