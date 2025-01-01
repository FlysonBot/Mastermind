from typing import Any, TypeVar

from requests import Response

from mastermind.libs.logs import ClientLogger
from mastermind.server.database import converter

T = TypeVar("T")
logger = ClientLogger("Unpack Response")


def unpack_response(response: Response, type: type) -> Any:
    """Structure the response data into the specified type.

    If the response status code is not 2xx, raise the corresponding exception.

    Args:
        response (Response): The response object from requests library.
        type (type): The type to structure the response data into.

    Returns:
        Any: The structured response data.

    Examples:
        >>> from requests import Response
        >>> from dataclasses import dataclass
        >>> response = Response()
        >>> response.status_code = 200
        >>> response.json = lambda: {"id": 1, "name": "John"}
        >>> @dataclass
        ... class User:
        ...     id: int
        ...     name: str
        >>> unpack_response(response, User)
        User(id=1, name='John')
        >>> response.status_code = 400
        >>> unpack_response(response, User)
        Traceback (most recent call last):
        ...
        requests.exceptions.HTTPError: 400 Client Error: None for url: None
    """
    if str(response.status_code).startswith("2"):
        return _unpack_response(response.json(), type)

    logger.error(f"Error {response.status_code}: {response.text}")
    response.raise_for_status()


def _unpack_response(data: T, type: type[T]) -> T:
    return converter.structure(data, type)
