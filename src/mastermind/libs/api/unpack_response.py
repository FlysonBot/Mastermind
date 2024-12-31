from typing import Any, TypeVar

from flask import Response

from mastermind.server.database import converter

T = TypeVar("T")


def unpack_response(request: Response, type: type) -> Any:
    return _unpack_response(request.get_json(), type)


def _unpack_response(data: T, type: type[T]) -> T:
    return converter.structure(data, type)
