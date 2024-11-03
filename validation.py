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
        # If the attribute exists, validate directly (or skip validation if not validated type)
        if hasattr(self, name):
            attr = super().__getattribute__(name)
            if isinstance(attr, ValidatedData):
                attr.validate(value)

        # If attribute doesn't exist, apply validation chain
        else:
            value = self._apply_validations(name, value)

        # Set the attribute (validated instance or original value if no validation needed)
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Retrieve attribute and return the underlying value for ValidatedData instances."""
        value = super().__getattribute__(name)
        
        while isinstance(value, ValidatedData):  # While it's a validated type
            value = value.get()  # Keep getting the inner value (peal off the validation)
        
        return value

    def _apply_validations(self, name: str, value: Any) -> Any:
        """
        Dynamically wrap `value` with ValidatedData subclasses based on attribute name.
        Chains multiple validations if needed (e.g., `Constant(NumberOfDots(value))`).
        """
        # Determine if a constant validation is needed
        validations = []
        
        if name.isupper():  # Attribute name is all upper case (a constant)
            validations.append(Constant)
        
        # Convert snake_case name to CamelCase for other specific validations
        class_name = ''.join(word.capitalize() for word in name.lower().split('_'))
        validation_class = globals().get(class_name)

        # Check if the class exists and is a ValidatedData subclass
        if validation_class and issubclass(validation_class, ValidatedData):
            validations.append(validation_class)

        # Apply validations in order (outermost to innermost wrapping)
        for validation in reversed(validations):
            value = validation(value)

        return value


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


# Example Usage
class GameSettings(BaseModel):
    """Class to manage game settings with validated attributes."""
    
    def __init__(self):
        # Initialize attributes (automatically applies validation if applicable)
        self.CONSTANT_VALUE = 42  # Will be wrapped as Constant
        self.number_of_dots = 5  # Will be wrapped as NumberOfDots
        self.number_of_colors = 3  # Will be wrapped as NumberOfColors


# Testing
if __name__ == "__main__":
    # Instance of the GameSettings class
    settings = GameSettings()

    print("Constant Value:", settings.CONSTANT_VALUE)  # Should print 42
    try:
        settings.CONSTANT_VALUE = 50  # Should raise ValidationError
    except ValidatedData.ValidationError as e:
        print("Validation Error:", e)

    print("Number of Dots:", settings.number_of_dots)  # Should print 5
    settings.number_of_dots = 10  # Valid modification
    print("Updated Number of Dots:", settings.number_of_dots)

    try:
        settings.number_of_dots = -1  # Should raise ValidationError
    except ValidatedData.ValidationError as e:
        print("Validation Error:", e)

    print("Number of Colors:", settings.number_of_colors)  # Should print 3
    settings.number_of_colors = 4  # Valid modification
    print("Updated Number of Colors:", settings.number_of_colors)

    try:
        settings.number_of_colors = 1  # Should raise ValidationError
    except ValidatedData.ValidationError as e:
        print("Validation Error:", e)
