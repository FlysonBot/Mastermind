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
        """Validate and set attribute, automatically applying ValidatedData if possible."""
        if hasattr(self, name):  # Check if the attribute already exists
            attr = super().__getattribute__(name)  # Retrieve the attribute
            if isinstance(attr, ValidatedData):  # Check if is validated type
                attr.validate(value)  # Validate the new value

        else:
            if not isinstance(value, ValidatedData):  # Check if is not validated type
                # If not, attempt to find a corresponding ValidatedData subclass
                validated_class = self._find_validated_class(name)

                if validated_class:  # If a matching ValidatedData subclass exists
                    value = validated_class(value)  # Initialize it with the value

        # Set the attribute (either validated instance or raw value if no validation class found)
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Retrieve attribute and return the underlying value for ValidatedData instances."""
        attr = super().__getattribute__(name)
        if isinstance(attr, ValidatedData):  # If it's a validated type
            return attr.get()  # Return the value using the get method
        return attr  # Otherwise return the attribute as is

    @staticmethod
    def _find_validated_class(name: str) -> Any:
        """
        Convert attribute name to class name and check if it's a ValidatedData subclass.
        For example, 'number_of_dots' -> 'NumberOfDots'.
        """
        if name.isupper():  # Attribute name is all upper case (a constant)
            return Constant  # Apply constant
        
        # Convert snake_case name to CamelCase
        class_name = ''.join(word.capitalize() for word in name.split('_'))

        # Check if a class with this name exists and is a subclass of ValidatedData
        return globals().get(class_name) if issubclass(globals().get(class_name, object), ValidatedData) else None


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

