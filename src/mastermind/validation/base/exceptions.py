class ValidationError(Exception):
    """
    The base class for all validation-related exceptions.
    """


class MissingParameterError(ValidationError):
    """
    Raised when a required parameter is missing.
    """


class TypeValidationError(ValidationError):
    """
    Raised when a value does not match the expected type.
    """


class InputConversionError(ValidationError):
    """
    Raised when a value cannot be converted to the expected type.
    """


class RangeError(ValidationError):
    """
    Raised when a value is outside the expected range.
    """


class InvalidModificationError(ValidationError):
    """
    Raised when a modification to a validated value is invalid.
    """
