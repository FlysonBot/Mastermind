import unittest

from src.validation.base.exceptions import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)
from src.validation.models.game_io import (
    ValidCombination,
    ValidFeedback,
    _GameValidationUtils,
)


class TestGameValidationUtils(unittest.TestCase):
    """Test suite for the _GameValidationUtils class"""

    def test_convert_valid_input(self):
        """Test that _GameValidationUtils.convert handles valid input"""
        self.assertEqual(_GameValidationUtils.convert("1,2,3"), (1, 2, 3))
        self.assertEqual(_GameValidationUtils.convert("123"), (1, 2, 3))

    def test_convert_invalid_input(self):
        """Test that _GameValidationUtils.convert raises an error for invalid input"""
        with self.assertRaises(InputConversionError) as context:
            _GameValidationUtils.convert("1,2,a")
        self.assertEqual(str(context.exception), "Invalid combination format")

        with self.assertRaises(InputConversionError) as context:
            _GameValidationUtils.convert("1 2 3")
        self.assertEqual(str(context.exception), "Invalid combination format")

    def test_validate_valid_arguments(self):
        """Test that _GameValidationUtils.validate_arguments validates the arguments"""

        class MockValidationModel:
            n_of_dots = 4
            n_of_colors = 6

        _GameValidationUtils.validate_arguments(MockValidationModel())
    
    def test_validate_invalid_arguments(self):
        """Test that _GameValidationUtils.validate_arguments raises errors for invalid arguments"""

        class MockValidationModel1:
            n_of_dots = 1
            n_of_colors = 1
        
        class MockValidationModel2:
            n_of_dots = 4
            n_of_colors = 1
        
        with self.assertRaises(RangeError) as context:
            _GameValidationUtils.validate_arguments(MockValidationModel1())
        self.assertEqual(str(context.exception), "Value must be greater than or equal to 2")

        with self.assertRaises(RangeError) as context:
            _GameValidationUtils.validate_arguments(MockValidationModel2())
        self.assertEqual(str(context.exception), "Value must be greater than or equal to 2")


class TestValidCombination(unittest.TestCase):
    """Test suite for the ValidCombination class"""

    def test_validate_value_with_valid_input(self):
        """Test that ValidCombination can validate valid combinations"""
        model = ValidCombination(3, 6)
        self.assertEqual(model.validate_value("1,2,3"), (1, 2, 3))
        self.assertEqual(model.validate_value("123"), (1, 2, 3))
        self.assertEqual(model.validate_value((1, 2, 3)), (1, 2, 3))
        self.assertEqual(model.validate_value([1, 2, 3]), (1, 2, 3))

    def test_validate_value_with_invalid_input(self):
        """Test that ValidCombination raises errors for invalid combinations"""
        model = ValidCombination(3, 6)

        with self.assertRaises(TypeValidationError) as context:
            model.validate_value(["1", "2", "3"])
        self.assertEqual(str(context.exception), "Dots must be integers")

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2))
        self.assertEqual(str(context.exception), "Combination must have 3 dots")

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2, 7))
        self.assertEqual(
            str(context.exception), "Dots must be between 1 and 6"
        )

        with self.assertRaises(TypeValidationError) as context:
            model.validate_value(True)
        self.assertEqual(
            str(context.exception), "A combination must be a tuple or list of integers"
        )

    def test_validate_combination(self):
        """Test that ValidCombination can validate the individual dots in a combination"""
        model = ValidCombination(3, 6)
        model.validate_combination((1, 2, 3))

        with self.assertRaises(RangeError) as context:
            model.validate_combination((1, 2, 7))
        self.assertEqual(
            str(context.exception), "Dots must be between 1 and 6"
        )

        with self.assertRaises(RangeError) as context:
            model.validate_combination((1, 2))
        self.assertEqual(str(context.exception), "Combination must have 3 dots")


class TestValidFeedback(unittest.TestCase):
    """Test suite for the ValidFeedback class"""

    def test_convert_valid_input(self):
        """Test that ValidFeedback.convert handles valid input"""
        model = ValidFeedback(4)
        self.assertEqual(model.convert("1,2"), (1, 2))
        self.assertEqual(model.convert("13"), (1, 3))
        self.assertEqual(model.convert((2, 2)), (2, 2))
        self.assertEqual(model.convert([3, 1]), (3, 1))

    def test_convert_invalid_input(self):
        """Test that ValidFeedback.convert raises an error for invalid input"""
        model = ValidFeedback(4)
        with self.assertRaises(InputConversionError) as context:
            model.convert("1,a")
        self.assertEqual(str(context.exception), "Invalid feedback format")

    def test_validate_value_with_valid_input(self):
        """Test that ValidFeedback can validate valid feedback"""
        model = ValidFeedback(4)
        self.assertEqual(model.validate_value("1,2"), (1, 2))
        self.assertEqual(model.validate_value("13"), (1, 3))
        self.assertEqual(model.validate_value((2, 2)), (2, 2))
        self.assertEqual(model.validate_value([3, 1]), [3, 1])

    def test_validate_value_with_invalid_input(self):
        """Test that ValidFeedback raises errors for invalid feedback"""
        model = ValidFeedback(4)

        with self.assertRaises(TypeValidationError) as context:
            model.validate_value("121")
        self.assertEqual(
            str(context.exception), "Feedback must be a tuple or list of two integers"
        )

        with self.assertRaises(ValueError) as context:
            model.validate_value((-1, 5))
        self.assertEqual(
            str(context.exception), "Feedback values must be between 0 and 4"
        )

        with self.assertRaises(ValueError) as context:
            model.validate_value((2, 3))
        self.assertEqual(str(context.exception), "Feedback values sum cannot exceed 4")

    def test_validate_arguments(self):
        """Test that ValidFeedback validates the arguments"""
        with self.assertRaises(RangeError) as context:
            ValidFeedback(-1)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 2"
        )


if __name__ == "__main__":
    unittest.main()
