from mastermind.libs.api import pack_response
from mastermind.server.api.app import app
from mastermind.server.api.game import retrieve_game_by_id


@app.route("/games/<str:game_id>/guess", methods=["POST"])
def guess(game_id: str):
    retrieve_game_by_id(game_id)

    # TODO: make GameService, attempt request, return response

    return pack_response({}), 201


# TODO: add get guess, post/get feedback, post undo, post redo
