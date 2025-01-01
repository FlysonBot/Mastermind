from typing import Literal

from flask import abort, request
from flask.wrappers import Response
from shortuuid import get_alphabet as shortuuid_alphabet

from mastermind.libs.api import RaiseErrorCode, pack_response, unpack_request
from mastermind.server.api.app import app
from mastermind.server.api.repository import (
    GameInfo,
    get_filter_func,
    retrieve_game_info,
)
from mastermind.server.database.models import Game, GameConfiguration
from mastermind.server.database.repository import GameRepository

game_repository = GameRepository()


@app.route("/games", methods=["POST"])
def create_game() -> tuple[Response, Literal[201]]:
    """API for creating a new game and returning its game id."""
    game_config: GameConfiguration = unpack_request(request, GameConfiguration)

    game: Game = Game(game_configuration=game_config)
    game_id: str = game_repository.add(game)

    return pack_response({"id": game_id}), 201


@app.route("/games/<str:game_id>", methods=["GET"])
def get_game_info(game_id: str) -> tuple[Response, Literal[201]]:
    """API for retrieving game information for a specific game given its id."""
    game: Game = retrieve_game_by_id(game_id)

    game_info: list[GameInfo] = retrieve_game_info(
        [(game_id, game)], get_filter_func(False)
    )

    return pack_response(game_info[0]), 201  # just the first result


@app.route("/games/<str:game_id>", methods=["DELETE"])
def delete_game(game_id: str) -> tuple[Literal[""], Literal[204]]:
    """API for deleting a game given its id."""
    retrieve_game_by_id(game_id)

    del game_repository[game_id]

    return "", 204


def retrieve_game_by_id(game_id: str) -> Game:
    """Utility function for retrieving a game by its id.
    
    Args:
        game_id (str): The id of the game to retrieve.

    Raises:
        404: If the game with the specified id does not exist.
        400: If the game id is invalid.
    
    Returns:
        Game: The game with the specified id.
    """
    with RaiseErrorCode(KeyError, 404, f"Game with id {game_id} does not exist"):
        if game_id not in game_repository and (
            len(game_id) != 6 or set(game_id).difference(set(shortuuid_alphabet()))
        ):
            abort(
                400,
                description=f"Invalid game id: {game_id}. A game id must has 6 characters and only contain characters in {shortuuid_alphabet()}",
            )

        return game_repository[game_id]
