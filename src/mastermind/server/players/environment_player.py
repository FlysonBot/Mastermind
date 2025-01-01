from mastermind.server.players.base_players import (
    CodeBreaker,
    CodeSetter,
    Combination,
    Feedback,
)


class EnvironmentSetter(CodeSetter):
    def obtain_feedback(self) -> Feedback: ...


class EnvironmentBreaker(CodeBreaker):
    def obtain_guess(self) -> Combination: ...
