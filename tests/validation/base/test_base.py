import unittest
from dataclasses import dataclass
from typing import Any, TypeVar

from src.validation.base.base import StateValidator, ValidationModel, Validator

T = TypeVar("T")


class TestValidator(unittest.TestCase):
    def test_validate_value_abstract_method(self):
        with self.assertRaises(TypeError):
            Validator[T]().validate_value(42)


class TestValidationModel(unittest.TestCase):
    def test_init_with_valid_kwargs(self):
        class ConcreteValidationModel(ValidationModel[int]):
            def validate_arguments(self) -> None:
                pass

            def validate_value(self, value: Any) -> int:
                return int(value)

        model = ConcreteValidationModel(a=1, b=2)
        self.assertEqual(model.a, 1)
        self.assertEqual(model.b, 2)

    def test_init_with_invalid_kwargs(self):
        class ConcreteValidationModel(ValidationModel[int]):
            def validate_arguments(self) -> None:
                if hasattr(self, "a") and self.a < 0:
                    raise ValueError("a must be non-negative")

            def validate_value(self, value: Any) -> int:
                return int(value)

        with self.assertRaises(ValueError) as context:
            ConcreteValidationModel(a=-1, b=2)
        self.assertEqual(str(context.exception), "a must be non-negative")


class TestStateValidator(unittest.TestCase):
    @dataclass
    class ConcreteStateValidator(StateValidator[int]):
        min_value: int = 0
        max_value: int = 100

        def validate_value(self, value: Any) -> int:
            value = int(value)
            if value < self.min_value or value > self.max_value:
                raise ValueError(
                    f"Value must be between {self.min_value} and {self.max_value}"
                )
            return value

        def validate_modifications(self, new_value: Any) -> int:
            value = self.validate_value(new_value)
            if value < self.min_value or value > self.max_value:
                raise ValueError(
                    f"New value must be between {self.min_value} and {self.max_value}"
                )
            return value

    def test_init_with_valid_value(self):
        validator = self.ConcreteStateValidator(50)
        self.assertEqual(validator.value, 50)

    def test_init_with_invalid_value(self):
        with self.assertRaises(ValueError) as context:
            self.ConcreteStateValidator(-1)
        self.assertEqual(str(context.exception), "Value must be between 0 and 100")

    def test_set_value_with_valid_value(self):
        validator = self.ConcreteStateValidator(50)
        validator.value = 75
        self.assertEqual(validator.value, 75)

    def test_set_value_with_invalid_value(self):
        validator = self.ConcreteStateValidator(50)
        with self.assertRaises(ValueError) as context:
            validator.value = -1
        self.assertEqual(str(context.exception), "New value must be between 0 and 100")


if __name__ == "__main__":
    unittest.main()
