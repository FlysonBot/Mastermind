from typing import Any, Optional, Union

import requests

from mastermind.server.database import converter

JSON = dict[str, Any]
Params = Union[JSON, list[tuple[str, Any]]]


class Request:
    base_url: str

    def __init__(self, path: str):
        self.path = path
        self.url = f"{self.base_url}{path}"

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
