from typing import Any, NamedTuple


class Response(NamedTuple):
    """A response from the server."""

    status: int
    message: str
    data: Any
