from mastermind.server.players._computer_utils import ComputerUtils
from mastermind.server.players.base_players import CodeBreaker, CodeSetter


class ComputerSetter(CodeSetter, ComputerUtils):
    def obtain_feedback(self):
        pass


class ComputerBreaker(CodeBreaker, ComputerUtils):
    def obtain_guess(self):
        pass
