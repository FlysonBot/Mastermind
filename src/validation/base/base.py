from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Validator(ABC, Generic[T]):
    """Base class for all validators."""

    @abstractmethod
    def validate_value(self, value: Any) -> T:
        """Validate and potentially transform the input value."""
        pass


class ValidationModel(Validator[T], ABC):
    """Stateless validator that only validates input."""

    def __init__(self, **kwargs) -> None:
        """Initialize with optional keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.validate_arguments()

    def validate_arguments(self) -> None:
        """Validate the keyword arguments."""
        pass


class StateValidator(Validator[T], ABC):
    """Validator that maintains state and validates modifications."""

    def __init__(self, value: Any):
        self._value = self.validate_value(value)

    @abstractmethod
    def validate_modifications(self, new_value: Any) -> None:
        """Validate modifications to the value."""
        pass

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = self.validate_modifications(new_value)
