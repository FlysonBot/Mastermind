from typing import Any, Callable, NamedTuple

from mastermind.libs.api.response import Response


class Request(NamedTuple):
    """A request to the server."""

    destination: Callable[["Request"], Response]
    data: Any

    def send(self) -> Response:
        """Send the request to the server."""
        return self.destination(self)
