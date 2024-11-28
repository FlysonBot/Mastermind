import unittest

from mastermind.validation.base.exceptions import (
    InputConversionError,
    RangeError,
)
from mastermind.validation.models._game_utils import GameValidationUtils


class TestGameValidationUtils(unittest.TestCase):
    """Test suite for the GameValidationUtils class"""

    def test_convert_valid_input(self):
        """Test that GameValidationUtils.convert handles valid input"""
        self.assertEqual(GameValidationUtils.convert("1,2,3"), (1, 2, 3))
        self.assertEqual(GameValidationUtils.convert("123"), (1, 2, 3))

    def test_convert_invalid_input(self):
        """Test that GameValidationUtils.convert raises an error for invalid input"""
        with self.assertRaises(InputConversionError) as context:
            GameValidationUtils.convert("1,2,a")
        self.assertEqual(str(context.exception), "Invalid input format")

        with self.assertRaises(InputConversionError) as context:
            GameValidationUtils.convert("1 2 3")
        self.assertEqual(str(context.exception), "Invalid input format")

    def test_validate_valid_arguments(self):
        """Test that GameValidationUtils.validate_arguments validates the arguments"""

        class MockValidationModel:
            n_of_dots = 4
            n_of_colors = 6

        GameValidationUtils.validate_arguments(MockValidationModel())

    def test_validate_invalid_arguments(self):
        """Test that GameValidationUtils.validate_arguments raises errors for invalid arguments"""

        class MockValidationModel1:
            n_of_dots = 1
            n_of_colors = 1

        class MockValidationModel2:
            n_of_dots = 4
            n_of_colors = 1

        with self.assertRaises(RangeError) as context:
            GameValidationUtils.validate_arguments(MockValidationModel1())
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 2"
        )

        with self.assertRaises(RangeError) as context:
            GameValidationUtils.validate_arguments(MockValidationModel2())
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 2"
        )


if __name__ == "__main__":
    unittest.main()
