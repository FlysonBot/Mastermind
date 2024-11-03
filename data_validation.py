from typing import Any
from abc import ABC, abstractmethod

# Fundamental Classes
class ValidatedData(ABC):
    """Base class for validated data types."""
    
    class ValidationError(Exception):
        """Custom exception for validation errors."""
        pass

    def __init__(self, value: Any) -> None:
        """Initialize with a value and validate it."""
        self.validate(value)  # Validate at initialization
        self.value = value  # Set the value if validation is successful
    
    def get(self) -> Any:
        """Return the stored value."""
        return self.value

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Abstract method to validate the value. Must be implemented by subclasses."""
        pass


class BaseModel:
    """
    Base class for models that use validated attributes.
    Overrides __getattribute__ and __setattr__ to enforce validation.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """Validate and set attribute."""
        if hasattr(self, name):  # Check if the attribute already exists
            attr = super().__getattribute__(name)  # Retrieve the attribute
            if isinstance(attr, ValidatedData):  # Check if is validated type
                attr.validate(value)  # Validate the new value
        
        # Set the attribute if validation is completed or not needed
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        # Retrieve the attribute
        attr = super().__getattribute__(name)
        if isinstance(attr, ValidatedData):  # Check if it's a validated type
            return attr.get()  # Return the value using the get method
        return attr  # Otherwise return the attribute as is


# ValidatedData Subclasses (Custom data types that are validated)
class Constant(ValidatedData):
    """A constant value that cannot be modified after initialization."""

    def validate(self, value: Any) -> None:
        """Ensure the constant value is not modified."""
        if hasattr(self, 'value'):  # Check if value is already set
            raise self.ValidationError("Cannot modify constant after initialization")


class NumberOfDots(ValidatedData):
    """Validated property for the number of dots."""
    
    def validate(self, value: Any) -> None:
        """Ensure the number of dots is a positive integer."""
        if not isinstance(value, int) or value < 2:
            raise self.ValidationError("Number of dots must be an integer greater than or equal to 2.")


class NumberOfColors(ValidatedData):
    """Validated property for the number of colors."""
    
    def validate(self, value: Any) -> None:
        """Ensure the number of colors is an integer of at least 2."""
        if not isinstance(value, int) or value < 2:
            raise self.ValidationError("Number of colors must be an integer greater than or equal to 2.")

