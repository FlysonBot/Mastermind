from inspect import stack
from typing import Any

from flask import Request, abort

from mastermind.server.database import converter

from ..logs import ServerLogger

logger = ServerLogger("Unpack Request")


def unpack_request(request: Request, type: type) -> Any:
    """Structure the request data into the specified type.

    When the request data cannot be structured into the specified type, a 400 Bad Request error is raised.

    Args:
        request (Request): The flask.request variable.
        type (type): The type to structure the request data into.

    Returns:
        Any: The structured request data.
    """
    try:
        return converter.structure(request.get_json(), type)  # type: ignore

    except Exception as e:
        caller = stack()[1].function
        error_message = f"Unable to unpack request data into type {type.__name__} (api: {caller})\n{e}"
        logger.error(error_message)
        abort(400, description=error_message)
