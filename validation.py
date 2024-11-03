from typing import Any
from abc import ABC, abstractmethod

# Fundamental Classes
class ValidatedData(ABC):
    """Base class for validated data types."""

    class ValidationError(Exception):
        """Custom exception for validation errors."""
        pass
    
    class MissingParameterError(Exception):
        """Custom exception for missing kwargs key."""
        pass

    def __init__(self, value: Any, **kwargs: Any) -> None:
        """Initialize with a value and optional additional parameters, then validate."""
        if kwargs:  # If there are kwargs
            self.kwargs = kwargs  # Store them
            self.validate_kwargs()  # And validate them
        
        self.validate(value)  # Validate on initialization
        self.value = value  # Store the main value


    def get(self) -> Any:
        """Return the main stored value only."""
        return self.value

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Abstract method to validate the value. Must be implemented by subclasses."""
        pass
    
    def validate_kwargs(self) -> None:
        """Abstract method to validate kwargs. Optionally implemented by subclasses."""
        pass


class BaseModel:
    """
    Base class for models that use validated attributes.
    Overrides __getattribute__ and __setattr__ to enforce validation.
    """

    def __setattr__(self, name: str, value: Any) -> None:
        """Validate and set attribute, automatically applying ValidatedData if possible."""
        # If the attribute already exists
        if hasattr(self, name):
            attr = super().__getattribute__(name)  # Get the attribute
            
            if isinstance(attr, ValidatedData):  # If is a validated type
                if isinstance(value, ValidatedData):  # If input is validated
                    if typeof(value) != typeof(attr):  # If not the same type
                        raise ValidationError("Cannot assign a different type to a validated attribute.")
                
                else:  # If input is not validated
                    attr.validate(value)  # Validate it

        # If attribute doesn't exist, verify if input is a validated type
        elif not isinstance(value, ValidatedData):
            # Try to find a suitable validated type from attribute name
            value = self._apply_validations(name, value)
        
        # If already validated, or cannot be validated, update the attribute
        super().__setattr__(name, value)

    def __getattribute__(self, name: str) -> Any:
        """Retrieve attribute and return the underlying value for ValidatedData instances."""
        value = super().__getattribute__(name)
        
        while isinstance(value, ValidatedData):  # While it's a validated type
            value = value.get()  # Keep getting the inner value (peel off the validation)
        
        return value

    def _apply_validations(self, name: str, value: Any) -> Any:
        """
        Dynamically wrap `value` with ValidatedData subclasses based on attribute name.
        Chains multiple validations if needed (e.g., `Constant(NumberOfDots(value))`).
        """
        # Determine if a constant validation is needed
        validations = []
        
        if name.isupper():  # Attribute name is all uppercase (a constant)
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
        """Ensure the constant value is not modified after initialization."""
        if hasattr(self, 'value'):
            raise self.ValidationError("Cannot modify constant after initialization.")

    def _modify(self, new_value: Any) -> None:
        """Private method to modify constant value for testing purposes."""
        self.value = new_value


class NumberOfDots(ValidatedData):
    """Validated property for the number of dots."""
    
    def validate(self, value: Any) -> None:
        """Ensure the number of dots is a positive integer."""
        if not isinstance(value, int):
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    raise self.ValidationError("Number of dots must be an integer greater than or equal to 2.")
            else:
                raise self.ValidationError("Number of dots must be an integer greater than or equal to 2.")
        
        if value < 2:
            raise self.ValidationError("Number of dots must be an integer greater than or equal to 2.")


class NumberOfColors(ValidatedData):
    """Validated property for the number of colors."""
    
    def validate(self, value: Any) -> None:
        """Ensure the number of colors is an integer of at least 2."""
        if not isinstance(value, int):
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    raise self.ValidationError("Number of colors must be an integer greater than or equal to 2.")
            else:
                raise self.ValidationError("Number of colors must be an integer greater than or equal to 2.")
        
        if value < 2:
            raise self.ValidationError("Number of colors must be an integer greater than or equal to 2.")


class NumberOfGuessesMade(ValidatedData):
    """Validated property for the number of guesses made during a game."""

    def validate(self, value: Any) -> None:
        """Ensure the number of guesses made is an integer of at least 0."""
        if not isinstance(value, int):
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    raise self.ValidationError("Number of guesses made must be an integer greater than or equal to 0.")
            else:
                raise self.ValidationError("Number of guesses made must be an integer greater than or equal to 0.")
        
        if value < 0:
            raise self.ValidationError("Number of guesses made must be an integer greater than or equal to 0.")


class MaximumAttemps(ValidatedData):
    """Validated property for the maximum number of attempts allowed per game."""

    def validate(self, value: Any) -> None:
        """Ensure the maximum number of attempts is an integer of at least 1."""
        if not isinstance(value, int):
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    raise self.ValidationError("Maximum number of attempts must be an integer greater than or equal to 1.")
            else:
                raise self.ValidationError("Maximum number of attempts must be an integer greater than or equal to 1.")
        
        if value < 1:
            raise self.ValidationError("Maximum number of attempts must be an integer greater than or equal to 1.")


class GameMode(ValidatedData):
    """Validated property for the game mode. Must be HvH, HvAI, AIvH, or AIvAI."""

    def validate(self, value: Any) -> None:
        """Ensure the game mode is one of the allowed values."""
        allowed_modes = ['HvH', 'HvAI', 'AIvH', 'AIvAI']
        if value not in allowed_modes:
            raise self.ValidationError(f"Game mode must be one of {allowed_modes}.")


class SecretCode(ValidatedData):
    """Validated property for the secret code."""

    def validate_kwargs(self) -> None:
        """Ensure the kwargs contain the required keys."""
        if 'number_of_dots' not in self.kwargs:
            raise self.MissingParameterError("Missing 'number_of_dots' parameter in kwargs.")
        if 'number_of_colors' not in self.kwargs:
            raise self.MissingParameterError("Missing 'number_of_colors' parameter in kwargs.")
        NumberOfDots(self.kwargs['number_of_dots'])  # Validation
        NumberOfColors(self.kwargs['number_of_colors'])  # Validation

    def validate(self, value: Any) -> None:
        """Ensure the secret code is a tuple of integers of the correct length."""

        if not isinstance(value, tuple):
            raise self.ValidationError("Secret code must be a tuple of integers.")
        
        if len(value) != self.kwargs['number_of_dots']:
            raise self.ValidationError(f"Secret code must have {self.kwargs['number_of_dots']} dots.")
        
        for dot in value:
            if not isinstance(dot, int) or dot < 1 or dot > self.kwargs['number_of_colors']:
                raise self.ValidationError("All dots in the secret code must be integers in the range [1, number_of_colors].")
        

class Booleans(ValidatedData):
    """Validated property for booleans."""

    def validate(self, value: Any) -> None:
        """Ensure the value is a boolean or None."""
        if value is not None and not isinstance(value, bool):
            raise self.ValidationError("Booleans must be either True, False, or None.")


class TrueFuse(ValidatedData):
    """Validated property of a boolean that cannot be set to False after initialization."""

    def validate(self, value: Any) -> None:
        """Ensure the fuse cannot be set to False after initialization."""
        if value is False and hasattr(self, 'value'):
            raise self.ValidationError("Fuse cannot be set to False after initialization.")
        if value is not True:
            raise self.ValidationError("Cannot set fuse to a non-boolean value.")


class FalseFuse(ValidatedData):
    """Validated property of a boolean that cannot be set to True after initialization."""

    def validate(self, value: Any) -> None:
        """Ensure the fuse cannot be set to True after initialization."""
        if value is True and hasattr(self, 'value'):
            raise self.ValidationError("Fuse cannot be set to True after initialization.")
        if value is not False:
            raise self.ValidationError("Cannot set fuse to a non-boolean value.")
