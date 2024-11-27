import unittest

from src.validation.base.exceptions import (
    InputConversionError,
    RangeError,
)
from src.validation.models.valid_feedback import ValidFeedback


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
        self.assertEqual(str(context.exception), "Invalid input format")

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

        with self.assertRaises(RangeError) as context:
            model.validate_value("121")
        self.assertEqual(
            str(context.exception), "Feedback must be a tuple or list of two integers"
        )

        with self.assertRaises(RangeError) as context:
            model.validate_value((-1, 4))
        self.assertEqual(str(context.exception), "Value -1 is not in range [0, 4]")

        with self.assertRaises(RangeError) as context:
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
