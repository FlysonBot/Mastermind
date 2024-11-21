from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Validator(ABC, Generic[T]):
    @abstractmethod
    def validate_value(self, value: Any) -> T:
        pass


class ValidationModel(Validator[T], ABC):
    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.validate_arguments()

    def validate_arguments(self) -> None:
        pass


class StateValidator(Validator[T], ABC):
    def __init__(self, value: Any):
        self._value = self.validate_value(value)

    @abstractmethod
    def validate_modifications(self, new_value: Any) -> None:
        pass

    @property
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = self.validate_modifications(new_value)
