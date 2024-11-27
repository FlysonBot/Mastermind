from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Validator(ABC, Generic[T]):
    """
    An abstract base class for all validators.

    Defines the `validate_value` method that must be implemented by subclasses.
    """

    @abstractmethod
    def validate_value(self, value: Any) -> T:
        """
        Validates the given value and returns the validated value.

        Args:
            value (Any): The value to be validated.

        Returns:
            T: The validated value.
        """
        pass


class ValidationModel(Validator[T], ABC):
    """
    An abstract base class for validation models.

    Provides a base implementation for initializing the validation model with keyword arguments and validating the arguments.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initializes the validation model with the given keyword arguments.

        Args:
            **kwargs: The keyword arguments to be used for initializing the validation model.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.validate_arguments()

    def validate_arguments(self) -> None:
        """
        Validates the arguments used to initialize the validation model.

        This method must be implemented by subclasses to perform any necessary validation.
        """
        pass


class StateValidator(Validator[T], ABC):
    """
    An abstract base class for state validators.

    Provides a base implementation for managing the state of a validated value, including validation of modifications.
    """

    def __init__(self, value: Any):
        """
        Initializes the state validator with the given value.

        Args:
            value (Any): The initial value to be validated and stored.
        """
        self._value = self.validate_value(value)

    @abstractmethod
    def validate_modifications(self, new_value: Any) -> None:
        """
        Validates the modification of the value.

        Args:
            new_value (Any): The new value to be validated.

        Raises:
            ValidationError: If the new value is invalid.
        """
        pass

    @property
    def value(self) -> T:
        """
        Returns the validated value.

        Returns:
            T: The validated value.
        """
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        """
        Sets the new value, validating the modification.

        Args:
            new_value (Any): The new value to be set.
        """
        self._value = self.validate_modifications(new_value)
