from typing import Literal, Optional

from flask import abort, request
from flask.wrappers import Response

from mastermind.libs.api import pack_response
from mastermind.server.api.app import app
from mastermind.server.api.game import retrieve_game_by_id
from mastermind.server.database.enum import PlayerRole


@app.route("/games/<string:game_id>/join", methods=["POST"])
def join_game(game_id: str) -> tuple[Response, Literal[201]]:
    retrieve_game_by_id(game_id)

    player_role: PlayerRole = retrieve_player_role(
        request.get_json().get("player_role", None)
    )

    # TODO: access management

    return pack_response({"player_role": player_role.value}), 201


def retrieve_player_role(player_role: Optional[str]) -> PlayerRole:
    if player_role is None:
        abort(400, description="missing player_role field")

    try:
        return PlayerRole(player_role)

    except ValueError:
        abort(400, description=f"invalid player_role: {player_role}")
