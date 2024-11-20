class ValidationError(Exception):
    """Base exception for validation errors."""

    pass


class MissingParameterError(ValidationError):
    """Raised when a required parameter is missing."""

    pass


class TypeValidationError(ValidationError):
    """Raised when a value is of incorrect type."""

    pass


class InputConversionError(ValidationError):
    """Raised when a value cannot be converted to the desired type"""

    pass


class RangeError(ValidationError):
    """Raised when a value is outside its allowed range."""

    pass


class InvalidModificationError(ValidationError):
    """Raised when attempting to modify an object in an invalid way."""

    pass

