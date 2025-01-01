from typing import Any, Optional, Union

import requests

from mastermind.server.database import converter

JSON = dict[str, Any]
Params = Union[JSON, list[tuple[str, Any]]]


class RequestURL:
    """A class for sending HTTP requests to a specified URL.

    Attributes:
        path (str): The path of the server endpoint to send the request to (i.e. "http://localhost:5000)
    """

    base_url: str

    def __init__(self, path: str) -> None:
        """Initialize a RequestURL object with the specified path.

        Args:
            path (str): The URL without the server address (i.e. "/api/v1/games")
        """
        self.path: str = path
        self.url: str = f"{self.base_url}{path}"

    def get(
        self, params: Optional[Params] = None, data: Optional[JSON] = None
    ) -> requests.Response:
        return requests.get(self.url, params=params, json=converter.unstructure(data))

    def post(
        self, data: Optional[JSON] = None, params: Optional[Params] = None
    ) -> requests.Response:
        return requests.post(self.url, json=converter.unstructure(data), params=params)

    def delete(
        self, params: Optional[Params] = None, data: Optional[JSON] = None
    ) -> requests.Response:
        return requests.delete(
            self.url, params=params, json=converter.unstructure(data)
        )

    def put(
        self, data: Optional[JSON] = None, params: Optional[Params] = None
    ) -> requests.Response:
        return requests.put(self.url, json=converter.unstructure(data), params=params)
