from inspect import stack
from typing import Any

from flask import Request, abort

from mastermind.libs.logs import ServerLogger
from mastermind.server.database import converter

logger = ServerLogger("Unpack Request")


def unpack_request(request: Request, type: type) -> Any:
    """Unpack the request data into the given type, with error handling."""
    try:
        return converter.structure(request.get_json(), type)  # type: ignore

    except Exception as e:
        caller = stack()[1].function
        error_message = f"Unable to unpack request data into type {type.__name__} (api: {caller})\n{e}"
        logger.error(error_message)
        abort(400, description=error_message)