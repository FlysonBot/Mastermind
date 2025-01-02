from contextlib import contextmanager
from inspect import stack
from typing import Generator

from flask import abort

from ..logs import ServerLogger

logger = ServerLogger("RaiseErrorCode")


@contextmanager
def RaiseErrorCode(
    exception_type: type, status_code: int, description: str
) -> Generator[None, None, None]:
    """A context manager that raises the specified error code if the specified exception occurs.

    Args:
        exception_type (type): The type of the exception to catch.
        status_code (int): The HTTP status code to return.
        description (str): The description of the error to return and log.

    Example:
        >>> with RaiseErrorCode(ValueError, 400, "Invalid input"):
        ...     raise ValueError("Invalid input")
        Traceback (most recent call last):
            ...
        werkzeug.exceptions.BadRequest: 400 Bad Request: Invalid input
    """
    try:
        yield

    except exception_type as e:  # type: ignore
        caller: str = stack()[2].function
        caller_parent: str = stack()[3].function if len(stack()) > 3 else "main"
        error_message: str = f"{description} (api: {caller_parent}/{caller})\n{e}"
        logger.error(error_message)
        abort(status_code, description=description)
