from mastermind.server.players._human_utils import HumanUtils
from mastermind.server.players.base_players import (
    CodeBreaker,
    CodeSetter,
    Combination,
    Feedback,
)


class HumanSetter(CodeSetter, HumanUtils):
    def obtain_feedback(self) -> Feedback: ...


class HumanBreaker(CodeBreaker, HumanUtils):
    def obtain_guess(self) -> Combination: ...
