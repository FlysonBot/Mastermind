import unittest
from numbers import Number
from typing import TypeVar

from mastermind.validation.base.exceptions import (
    InputConversionError,
    RangeError,
    TypeValidationError,
)
from mastermind.validation.base.numeric import (
    ConstrainedFloat,
    ConstrainedInteger,
    NumberRangeModel,
)

T = TypeVar("T", bound=Number)


class TestNumberRangeModel(unittest.TestCase):
    """Test suite for the NumberRangeModel class"""

    class ModifiedNumberRangeModel(NumberRangeModel[T]):
        def convert(self, value: str) -> T:
            """Convert the input string to the desired type."""
            try:
                return float(value)
            except ValueError as e:
                raise InputConversionError("Invalid input for float conversion") from e

    def test_init_with_valid_range(self):
        """Test that NumberRangeModel can be initialized with valid range constraints"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        self.assertEqual(model.gt, 0.0)
        self.assertEqual(model.lt, 10.0)
        self.assertIsNone(model.ge)
        self.assertIsNone(model.le)

    def test_init_with_invalid_range(self):
        """Test that NumberRangeModel raises an error with invalid range constraints"""
        with self.assertRaises(ValueError) as context:
            self.ModifiedNumberRangeModel[float](gt=0.0, ge=1.0)
        self.assertEqual(str(context.exception), "gt and ge cannot be used together")

        with self.assertRaises(ValueError) as context:
            self.ModifiedNumberRangeModel[float](lt=0.0, le=1.0)
        self.assertEqual(str(context.exception), "lt and le cannot be used together")

        with self.assertRaises(ValueError) as context:
            self.ModifiedNumberRangeModel[float](ge=10.0, lt=5.0)
        self.assertEqual(
            str(context.exception),
            "Range maximum cannot be less than or equal to minimum",
        )

    def test_validate_value_with_valid_number(self):
        """Test that NumberRangeModel can validate a valid numeric value"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        self.assertEqual(model.validate_value(5.0), 5.0)

    def test_validate_value_with_invalid_number_1(self):
        # sourcery skip: class-extract-method
        """Test that NumberRangeModel raises an error with an invalid numeric value"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        with self.assertRaises(RangeError) as context:
            model.validate_value(-1.0)
        self.assertEqual(str(context.exception), "Value must be greater than 0.0")

        with self.assertRaises(RangeError) as context:
            model.validate_value(10.0)
        self.assertEqual(str(context.exception), "Value must be less than 10.0")

    def test_validate_value_with_invalid_number_2(self):
        """Test that NumberRangeModel raises an error with an invalid numeric value"""
        model = self.ModifiedNumberRangeModel[float](ge=0.0, le=10.0)
        with self.assertRaises(RangeError) as context:
            model.validate_value(-1.0)
        self.assertEqual(
            str(context.exception), "Value must be greater than or equal to 0.0"
        )

        with self.assertRaises(RangeError) as context:
            model.validate_value(10.1)
        self.assertEqual(
            str(context.exception), "Value must be less than or equal to 10.0"
        )

    def test_validate_value_with_valid_string(self):
        """Test that NumberRangeModel can validate a valid string value"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        self.assertEqual(model.validate_value("5.0"), 5.0)

    def test_validate_value_with_invalid_string(self):
        """Test that NumberRangeModel raises an error with an invalid string value"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        with self.assertRaises(InputConversionError) as context:
            model.validate_value("invalid")
        self.assertEqual(str(context.exception), "Invalid input for float conversion")

    def test_validate_value_with_non_number_type(self):
        """Test that NumberRangeModel raises an error with a non-numeric value"""
        model = self.ModifiedNumberRangeModel[float](gt=0.0, lt=10.0)
        with self.assertRaises(TypeValidationError) as context:
            model.validate_value([1, 2, 3])
        self.assertEqual(str(context.exception), "Invalid type for number validation")


class TestConstrainedInteger(unittest.TestCase):
    """Test suite for the ConstrainedInteger class"""

    def test_convert_valid_string(self):
        """Test that ConstrainedInteger can convert a valid string to an integer"""
        model = ConstrainedInteger(gt=0, lt=10)
        self.assertEqual(model.convert("5"), 5)

    def test_convert_invalid_string(self):
        """Test that ConstrainedInteger raises an error with an invalid string"""
        model = ConstrainedInteger(gt=0, lt=10)
        with self.assertRaises(InputConversionError) as context:
            model.convert("invalid")
        self.assertEqual(str(context.exception), "Invalid input for integer conversion")


class TestConstrainedFloat(unittest.TestCase):
    """Test suite for the ConstrainedFloat class"""

    def test_convert_valid_string(self):
        """Test that ConstrainedFloat can convert a valid string to a float"""
        model = ConstrainedFloat(gt=0.0, lt=10.0)
        self.assertEqual(model.convert("5.0"), 5.0)

    def test_convert_invalid_string(self):
        """Test that ConstrainedFloat raises an error with an invalid string"""
        model = ConstrainedFloat(gt=0.0, lt=10.0)
        with self.assertRaises(InputConversionError) as context:
            model.convert("invalid")
        self.assertEqual(str(context.exception), "Invalid input for float conversion")


if __name__ == "__main__":
    unittest.main()
