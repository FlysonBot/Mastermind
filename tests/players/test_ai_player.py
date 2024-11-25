import unittest

from src.game.game import Game
from src.players.ai_player import AICodeCracker, AICodeSetter
from src.validation.models.valid_combination import ValidCombination


class TestAICodeSetter(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "AIvH")
        self.code_setter = AICodeSetter(self.game)

    def test_set_secret_code(self):
        self.code_setter.set_secret_code()
        self.assertTrue(hasattr(self.code_setter, "SECRET_CODE"))
        ValidCombination(4, 6).validate_value(self.code_setter.SECRET_CODE)

    def test_get_feedback(self):
        self.code_setter.SECRET_CODE = (1, 2, 3, 4)
        self.assertEqual(self.code_setter.get_feedback((1, 2, 3, 4)), (4, 0))
        self.assertEqual(self.code_setter.get_feedback((1, 2, 4, 3)), (2, 2))
        self.assertEqual(self.code_setter.get_feedback((5, 5, 5, 5)), (0, 0))

    def test_get_feedback_without_secret_code(self):
        with self.assertRaises(NotImplementedError):
            self.code_setter.get_feedback((1, 2, 3, 4))


class TestAICodeCracker(unittest.TestCase):
    def setUp(self):
        self.game = Game(6, 4, 10, "AIvH")
        self.code_cracker = AICodeCracker(self.game, "You won!", "You lost.")

    # TODO: Add tests for the AI solver logic when implemented
    pass


if __name__ == "__main__":
    unittest.main()
