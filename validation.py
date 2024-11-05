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
        
        # Validate on initialization and update the value
        self.value = self.validate(value)  # sometimes validate() return a different value

    def get(self) -> Any:
        """Return the main stored value only."""
        return self.value

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Abstract method to validate the value. Must be implemented by subclasses."""
        return value
    
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
                    if type(value) is not type(attr):  # If not the same type
                        raise ValidationError("Cannot assign a different type to a validated attribute.")
                    # Continue to super().__setattr__ below
                
                else:  # If input is not validated
                    attr.value = attr.validate(value)  # Validate and update
                    return  # return to avoid invoking super().__setattr__

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
        return value

    def _modify(self, new_value: Any) -> None:
        """Private method to modify constant value for testing purposes."""
        self.value = new_value


class GameMode(ValidatedData):
    """Validated property for the game mode. Must be HvH, HvAI, AIvH, or AIvAI."""

    def validate(self, value: Any) -> None:
        """Ensure the game mode is one of the allowed values."""
        allowed_modes = ['HvH', 'HvAI', 'AIvH', 'AIvAI']
        if value not in allowed_modes:
            raise self.ValidationError(f"Game mode must be one of {allowed_modes}.")
        return value


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
        
        return value

class Booleans(ValidatedData):
    """Validated property for booleans."""

    def validate(self, value: Any) -> None:
        """Ensure the value is a boolean or None."""
        if value not in [True, False, None]:
            raise self.ValidationError("Booleans must be either True, False, or None.")
        return value


class TrueFuse(ValidatedData):
    """Validated property of a boolean that cannot be set to False after initialization."""

    def validate(self, value: Any) -> None:
        """Ensure the fuse cannot be set to False after initialization."""
        if value is False:
            if hasattr(self, 'value'):  # If already initialized
                raise self.ValidationError("TrueFuse cannot be set to False after initialization.")
            return  # otherwise it is valid, return to skip the next if statement
        
        if value is not True:  # If value is not True or False
            raise self.ValidationError("Cannot set fuse to a non-boolean value.")
        
        return value


class FalseFuse(ValidatedData):
    """Validated property of a boolean that cannot be set to True after initialization."""

    def validate(self, value: Any) -> None:
        """Ensure the fuse cannot be set to True after initialization."""
        if value is True:
            if hasattr(self, 'value'):
                raise self.ValidationError("FalseFuse cannot be set to True after initialization.")
            return
        if value is not False:
            raise self.ValidationError("Cannot set fuse to a non-boolean value.")
        
        return value


class ConfinedInteger(ValidatedData):
    """Validated property for an integer that must be within a specified range."""

    def validate_kwargs(self) -> None:
        """Ensure the kwargs contain the required keys."""
        acceptable_args = ['lt', 'le', 'gt', 'ge']  # lt = less than, le = less than or equals to, etc.
        
        if len(self.kwargs) == 0:
            raise self.MissingParameterError("Must provide at least one of 'lt', 'le', 'gt', or 'ge' parameter in kwargs.")
        
        for arg in self.kwargs:
            if arg not in acceptable_args:
                raise self.ValidationError(f"Invalid argument '{arg}'. Must be one of {acceptable_args} and cannot be repeated.")
            acceptable_args.remove(arg)  # Remove the argument from the list of acceptable args
        
        if ('lt' in self.kwargs and 'le' in self.kwargs) or ('gt' in self.kwargs and 'ge' in self.kwargs):
            raise self.ValidationError("Cannot have both 'lt' and 'le' or 'gt' and 'ge' in kwargs.")
        
        lower_limit = self.kwargs.get('ge', self.kwargs.get('gt', float('-inf')))
        upper_limit = self.kwargs.get('le', self.kwargs.get('lt', float('inf')))
        if lower_limit > upper_limit:
            raise self.ValidationError("Lower limit cannot be higher than upper limit.")
    
    def validate(self, value: Any) -> None:
        """Ensure the value is an integer within the specified range."""
        # add support for converting string representation to int
        if not isinstance(value, int):
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    raise self.ValidationError("Value must be an integer.")
            else:
                raise self.ValidationError("Value must be an integer.")
        
        # Validate range
        if 'le' in self.kwargs and value > self.kwargs['le']:
            raise self.ValidationError(f"Value must be less than or equal to {self.kwargs['le']}.")
        if 'lt' in self.kwargs and value >= self.kwargs['lt']:
            raise self.ValidationError(f"Value must be less than {self.kwargs['lt']}.")
        if 'ge' in self.kwargs and value < self.kwargs['ge']:
            raise self.ValidationError(f"Value must be greater than or equal to {self.kwargs['ge']}.")
        if 'gt' in self.kwargs and value <= self.kwargs['gt']:
            raise self.ValidationError(f"Value must be greater than {self.kwargs['gt']}.")
        
        return value

class NumberOfDots(ConfinedInteger):
    """Validated property for the number of dots."""
    
    def __init__(self, value: Any) -> None:
        """Initialize with a value and provide a constrain"""
        super().__init__(value, ge=2)


class NumberOfColors(ConfinedInteger):
    """Validated property for the number of colors."""
    
    def __init__(self, value: Any) -> None:
        """Initialize with a value and provide a constrain"""
        super().__init__(value, ge=2)


class NumberOfGuessesMade(ConfinedInteger):
    """Validated property for the number of guesses made during a game."""

    def __init__(self, value: Any) -> None:
        """Initialize with a value and provide a constrain"""
        super().__init__(value, ge=0)


class MaximumAttempts(ConfinedInteger):
    """Validated property for the maximum number of attempts allowed per game."""

    def __init__(self, value: Any) -> None:
        """Initialize with a value and provide a constrain"""
        super().__init__(value, ge=1)

