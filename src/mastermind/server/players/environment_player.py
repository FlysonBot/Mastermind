from mastermind.server.players.base_players import CodeBreaker, CodeSetter


class EnvironmentSetter(CodeSetter):
    def obtain_feedback(self):
        pass


class EnvironmentBreaker(CodeBreaker):
    def obtain_guess(self):
        pass
