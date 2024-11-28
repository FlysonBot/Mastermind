import unittest
from typing import Any, TypeVar

from mastermind.validation.base.base import StateValidator, ValidationModel, Validator

T = TypeVar("T")


class TestValidator(unittest.TestCase):
    """Test suite for the Validator class"""

    def test_validate_value_abstract(self):
        """Test that validate_value is an abstract method"""
        with self.assertRaises(TypeError):
            Validator().validate_value(value=42)


class TestValidationModel(unittest.TestCase):
    """Test suite for the ValidationModel class"""

    def test_init_with_valid_kwargs(self):
        """Test that ValidationModel can be initialized with valid keyword arguments"""

        class ConcreteValidationModel(ValidationModel[int]):
            validate_value = None
            validate_arguments = lambda self: None  # noqa: E731

        model = ConcreteValidationModel(a=1, b=2, c=3)
        self.assertEqual(model.a, 1)
        self.assertEqual(model.b, 2)
        self.assertEqual(model.c, 3)

    def test_init_with_invalid_kwargs(self):
        """Test that ValidationModel raises an error with invalid keyword arguments"""

        class ConcreteValidationModel(ValidationModel[int]):
            validate_value = None

            def validate_arguments(self):
                if hasattr(self, "a") and self.a < 0:
                    raise ValueError("a must be non-negative")

        with self.assertRaises(ValueError) as context:
            ConcreteValidationModel(a=-1, b=2)

        self.assertEqual(str(context.exception), "a must be non-negative")

    def test_validate_arguments_abstract(self):
        """Test that validate_arguments is an abstract method"""
        with self.assertRaises(TypeError):
            ValidationModel[int]()


class TestStateValidator(unittest.TestCase):
    """Test suite for the StateValidator class"""

    def test_init_with_valid_value(self):
        """Test that StateValidator can be initialized with a valid value"""

        class ConcreteStateValidator(StateValidator[int]):
            validate_modifications = lambda self, new_value: None  # noqa: E731

            def validate_value(self, value: Any) -> int:
                return int(value)

        validator = ConcreteStateValidator(42)
        self.assertEqual(validator.value, 42)

    def test_init_with_invalid_value(self):
        """Test that StateValidator raises an error with an invalid value"""

        class ConcreteStateValidator(StateValidator[int]):
            validate_modifications = lambda self, new_value: None  # noqa: E731

            def validate_value(self, value: Any) -> None:
                if value < 0:
                    raise ValueError("Value must be non-negative")

        with self.assertRaises(ValueError) as context:
            ConcreteStateValidator(-1)

        self.assertEqual(str(context.exception), "Value must be non-negative")

    def test_value_property(self):
        """Test that the value property works as expected"""

        class ConcreteStateValidator(StateValidator[int]):
            validate_modifications = lambda self, new_value: None  # noqa: E731

            def validate_value(self, value: Any) -> int:
                return int(value)

        validator = ConcreteStateValidator(42)
        self.assertEqual(validator.value, 42)

    def test_value_setter_with_valid_value(self):
        """Test that the value setter works with a valid value"""

        class ConcreteStateValidator(StateValidator[int]):
            def validate_value(self, value: Any) -> int:
                return int(value)

            def validate_modifications(self, new_value: Any) -> int:
                return int(new_value)

        validator = ConcreteStateValidator(42)
        validator.value = 50
        self.assertEqual(validator.value, 50)

    def test_value_setter_with_invalid_value(self):
        """Test that the value setter raises an error with an invalid value"""

        class ConcreteStateValidator(StateValidator[int]):
            def validate_value(self, value: Any) -> int:
                return int(value)

            def validate_modifications(self, new_value: Any) -> None:
                if new_value < 0:
                    raise ValueError("Value must be non-negative")

        validator = ConcreteStateValidator(42)
        with self.assertRaises(ValueError) as context:
            validator.value = -10

        self.assertEqual(str(context.exception), "Value must be non-negative")

    def test_validate_modifications_abstract(self):
        """Test that validate_modifications is an abstract method"""
        with self.assertRaises(TypeError):
            StateValidator[int](42)


if __name__ == "__main__":
    unittest.main()
