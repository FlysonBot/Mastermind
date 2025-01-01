from typing import Any

from flask import Response, jsonify

from mastermind.server.database import converter


def pack_response(data: Any) -> Response:
    """Unstructure data into a flask-compatible JSON response."""
    return jsonify(converter.unstructure(data))
