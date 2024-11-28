class ValidationError(Exception):
    """
    The base class for all validation-related exceptions.
    """

    pass


class MissingParameterError(ValidationError):
    """
    Raised when a required parameter is missing.
    """

    pass


class TypeValidationError(ValidationError):
    """
    Raised when a value does not match the expected type.
    """

    pass


class InputConversionError(ValidationError):
    """
    Raised when a value cannot be converted to the expected type.
    """

    pass


class RangeError(ValidationError):
    """
    Raised when a value is outside the expected range.
    """

    pass


class InvalidModificationError(ValidationError):
    """
    Raised when a modification to a validated value is invalid.
    """

    pass
