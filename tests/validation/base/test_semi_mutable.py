import unittest

from mastermind.validation.base.exceptions import (
    InvalidModificationError,
    TypeValidationError,
)
from mastermind.validation.base.semi_mutable import TrueFuse


class TestTrueFuse(unittest.TestCase):
    """Test suite for the TrueFuse class"""

    def test_validate_value_with_valid_boolean(self):
        """Test that TrueFuse can be initialized with a valid boolean value"""
        validator = TrueFuse(True)
        self.assertTrue(validator.value)

        validator = TrueFuse(False)
        self.assertFalse(validator.value)

        with self.assertRaises(TypeValidationError):
            validator = TrueFuse(None)
            self.assertIsNone(validator.value)

    def test_validate_value_with_invalid_type(self):
        """Test that TrueFuse raises an error with a non-boolean value"""
        with self.assertRaises(TypeValidationError) as context:
            TrueFuse(42)
        self.assertEqual(
            str(context.exception), "TrueFuse can only be initialized to True or False"
        )

        with self.assertRaises(TypeValidationError) as context:
            TrueFuse("True")
        self.assertEqual(
            str(context.exception), "TrueFuse can only be initialized to True or False"
        )

    def test_validate_modifications_with_valid_value(self):
        """Test that TrueFuse can be modified to True"""
        validator = TrueFuse(False)
        validator.value = True
        self.assertTrue(validator.value)

        validator = TrueFuse(True)
        validator.value = True
        self.assertTrue(validator.value)

    def test_validate_modifications_with_invalid_value(self):
        """Test that TrueFuse raises an error when modified to False"""
        validator = TrueFuse(True)
        with self.assertRaises(InvalidModificationError) as context:
            validator.value = False
        self.assertEqual(
            str(context.exception), "TrueFuse can only be modified to True"
        )

        validator = TrueFuse(False)
        with self.assertRaises(InvalidModificationError) as context:
            validator.value = False
        self.assertEqual(
            str(context.exception), "TrueFuse can only be modified to True"
        )


if __name__ == "__main__":
    unittest.main()
