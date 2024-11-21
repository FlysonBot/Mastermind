class ValidationError(Exception):
    pass


class MissingParameterError(ValidationError):
    pass


class TypeValidationError(ValidationError):
    pass


class InputConversionError(ValidationError):
    pass


class RangeError(ValidationError):
    pass


class InvalidModificationError(ValidationError):
    pass
