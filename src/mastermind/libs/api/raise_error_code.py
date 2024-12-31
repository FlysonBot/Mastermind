from contextlib import contextmanager
from inspect import stack
from typing import Generator

from flask import abort

from mastermind.libs.logs import ServerLogger

logger = ServerLogger("RaiseErrorCode")


@contextmanager
def RaiseErrorCode(
    exception_type: type, status_code: int, description: str
) -> Generator[None, None, None]:
    """Raise the specified error code if the given exception occurs.

    Args:
        exception_type (type): The type of the exception to catch.
        status_code (int): The HTTP status code to return.
        description (str): The description of the error to return and log.
    """
    try:
        yield

    except exception_type as e:  # type: ignore
        caller = stack()[2].function
        error_message = f"{description} (api: {caller})\n{e}"
        logger.error(error_message)
        abort(status_code, description=description)
