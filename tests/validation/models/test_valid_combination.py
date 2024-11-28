import unittest

from mastermind.validation.base.exceptions import (
    RangeError,
    TypeValidationError,
)
from mastermind.validation.models.valid_combination import ValidCombination


class TestValidCombination(unittest.TestCase):
    """Test suite for the ValidCombination class"""

    def test_validate_value_with_valid_input(self):
        """Test that ValidCombination can validate valid combinations"""
        model = ValidCombination(3, 6)
        self.assertEqual(model.validate_value("1,2,3"), (1, 2, 3))
        self.assertEqual(model.validate_value("123"), (1, 2, 3))
        self.assertEqual(model.validate_value((1, 2, 3)), (1, 2, 3))
        self.assertEqual(model.validate_value([1, 2, 3]), (1, 2, 3))
        self.assertEqual(model.validate_value("6,6,6"), (6, 6, 6))
        self.assertEqual(model.validate_value("4,4,5"), (4, 4, 5))

    def test_validate_value_with_invalid_input(self):
        """Test that ValidCombination raises errors for invalid combinations"""
        model = ValidCombination(3, 6)

        with self.assertRaises(TypeValidationError) as context:
            model.validate_value(["1", "2", "3"])
        self.assertEqual(str(context.exception), "Input must be consist of integers")

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2))
        self.assertEqual(str(context.exception), "Combination must have 3 dots")

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2, 7))
        self.assertEqual(str(context.exception), "Value 7 is not in range [1, 6]")

        with self.assertRaises(TypeValidationError) as context:
            model.validate_value(True)
        self.assertEqual(
            str(context.exception), "A combination must be a tuple or list of integers"
        )

    def test_validate_combination(self):
        """Test that ValidCombination can validate the individual dots in a combination"""
        model = ValidCombination(3, 6)
        model.validate_value((1, 2, 3))

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2, 7))
        self.assertEqual(str(context.exception), "Value 7 is not in range [1, 6]")

        with self.assertRaises(RangeError) as context:
            model.validate_value((1, 2))
        self.assertEqual(str(context.exception), "Combination must have 3 dots")


if __name__ == "__main__":
    unittest.main()
