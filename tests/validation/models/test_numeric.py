import unittest

from mastermind.validation.base.exceptions import RangeError
from mastermind.validation.models.numeric import (
    MaximumAttempts,
    NumberOfColors,
    NumberOfDots,
    NumberOfGuessesMade,
)


class TestNumericValidationModels(unittest.TestCase):
    """Test suite for the numeric validation models"""

    def test_number_of_dots_valid(self):
        """Test that NumberOfDots can validate valid values"""
        model = NumberOfDots()
        self.assertEqual(model.validate_value(2), 2)
        self.assertEqual(model.validate_value(3), 3)

    def test_number_of_dots_invalid(self):
        """Test that NumberOfDots raises an error for invalid values"""
        model = NumberOfDots()
        with self.assertRaises(RangeError) as context:
            model.validate_value(1)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 2"
        )

    def test_number_of_colors_valid(self):
        """Test that NumberOfColors can validate valid values"""
        model = NumberOfColors()
        self.assertEqual(model.validate_value(2), 2)
        self.assertEqual(model.validate_value(3), 3)

    def test_number_of_colors_invalid(self):
        """Test that NumberOfColors raises an error for invalid values"""
        model = NumberOfColors()
        with self.assertRaises(RangeError) as context:
            model.validate_value(1)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 2"
        )

    def test_number_of_guesses_made_valid(self):
        """Test that NumberOfGuessesMade can validate valid values"""
        model = NumberOfGuessesMade()
        self.assertEqual(model.validate_value(0), 0)
        self.assertEqual(model.validate_value(1), 1)
        self.assertEqual(model.validate_value(10), 10)

    def test_number_of_guesses_made_invalid(self):
        """Test that NumberOfGuessesMade raises an error for invalid values"""
        model = NumberOfGuessesMade()
        with self.assertRaises(RangeError) as context:
            model.validate_value(-1)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 0"
        )

    def test_maximum_attempts_valid(self):
        """Test that MaximumAttempts can validate valid values"""
        model = MaximumAttempts()
        self.assertEqual(model.validate_value(1), 1)
        self.assertEqual(model.validate_value(2), 2)
        self.assertEqual(model.validate_value(10), 10)

    def test_maximum_attempts_invalid(self):
        """Test that MaximumAttempts raises an error for invalid values"""
        model = MaximumAttempts()
        with self.assertRaises(RangeError) as context:
            model.validate_value(0)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 1"
        )


if __name__ == "__main__":
    unittest.main()
