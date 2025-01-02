from ._computer_utils import ComputerUtils
from .base_players import (
    CodeBreaker,
    CodeSetter,
    Combination,
    Feedback,
)


class ComputerSetter(CodeSetter, ComputerUtils):
    def obtain_feedback(self) -> Feedback: ...


class ComputerBreaker(CodeBreaker, ComputerUtils):
    def obtain_guess(self) -> Combination: ...
