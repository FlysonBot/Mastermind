from functools import partial
from typing import Any, Callable, Iterable, Literal, Optional

from flask import request
from flask.wrappers import Response

from mastermind.libs.api import pack_response

from ..database.models import Game
from ..database.repository import GameRepository
from .app import app

game_repository = GameRepository()

GameInfo = dict[str, Any]
GameID = str
GameIdPair = tuple[GameID, Game]
GameInfoLookupFunc = Callable[[GameIdPair], Any]


@app.route("/games", methods=["GET"])
def api_list_game_info() -> tuple[Response, Literal[200]]:
    """API to list all the games in the game repository with their information.

    All request parameters are optional and passed as query parameters.

    Args:
        only_continuable (bool): Whether to only include games that had not ended.
        retrieve_all (bool): Whether to turn on blacklist mode (retrieve all except excluded keys).
        include (list[str]): A list of keys to include in the response (used in whitelist mode).
        exclude (list[str]): A list of keys to exclude from the response (used in blacklist mode).

    Returns:
        Response: A response containing a list of game information.
    """

    only_continuable: bool = request.args.get("only_continuable") is not None
    retrieve_all: bool = request.args.get("retrieveAll") is not None
    includes: set[str] = set(request.args.getlist("include") or [])
    excludes: set[str] = set(request.args.getlist("exclude") or [])

    games: list[GameIdPair] = list_games(only_continuable)
    filter_func: GameInfoLookupFunc = get_filter_func(retrieve_all, includes, excludes)

    result: list[GameInfo] = retrieve_game_info(games, filter_func)
    return pack_response(result), 200


def list_games(only_continuable: bool = False) -> list[GameIdPair]:
    """Lists all the game in the game repository, along with their ids.

    Args:
        only_continuable (bool): Whether to only include games that had not ended.

    Returns:
        list[GameIdPair]: A list of (id, game) pairs.
    """

    return (
        list(game_repository)
        if only_continuable
        else filter_continuable(list(game_repository))
    )


def filter_continuable(game_id_pairs: list[GameIdPair]) -> list[GameIdPair]:
    """Filters out games that had ended from the given list of games.

    Args:
        game_id_pairs (list[GameIdPair]): A list of (id, game) pairs to filter.

    Returns:
        list[GameIdPair]: A list of (id, game) pairs that have not ended.
    """

    return [
        game_id_pair
        for game_id_pair in game_id_pairs
        if not game_id_pair[1].game_state.game_over
    ]


def get_filter_func(
    blacklist: bool,
    includes: Optional[set[str]] = None,
    excludes: Optional[set[str]] = None,
) -> GameInfoLookupFunc:
    """Generate a function to filter the game information, based on the filter parameters.

    Args:
        blacklist (bool): Whether to use blacklist mode (retrieve all except excluded keys).
        includes (set[str]): A set of keys to include in the response (used in whitelist mode).
        excludes (set[str]): A set of keys to exclude from the response (used in blacklist mode).

    Returns:
        GameInfoLookupFunc: A function that takes a (id, game) pair and returns a dictionary of game information.
    """
    return (
        partial(_exclude, exclude=(excludes or set()))
        if blacklist
        else partial(_include, include=(includes or set()))
    )


def retrieve_game_info(
    games: list[GameIdPair], filter_func: Callable[[GameIdPair], GameInfo]
) -> list[GameInfo]:
    """Retrieve the game information using the given filtering function.

    Args:
        games (list[GameIdPair]): A list of (id, game) pairs to retrieve information for.
        filter_func (Callable[[GameIdPair], GameInfo]): A function that takes a (id, game) pair and returns a dictionary of game information.

    Returns:
        list[GameInfo]: A list of dictionaries containing game information.
    """
    return [filter_func(game) for game in games]


def _exclude(game: GameIdPair, exclude: set[str]) -> GameInfo:
    """Include all but the excluded keys."""
    return {
        key: lookup_func(game)
        for key, lookup_func in info_lookup.items()
        if key not in exclude
    }


def _include(game: GameIdPair, include: set[str]) -> GameInfo:
    """Include only the included keys."""
    return {
        key: lookup_func(game)
        for key, lookup_func in info_lookup.items()
        if key in include and key in valid_keys
    }


info_lookup: dict[str, GameInfoLookupFunc] = {
    "id": lambda pair: pair[0],
    "number_of_colors": lambda pair: pair[1].game_configuration.NUMBER_OF_COLORS,
    "number_of_dots": lambda pair: pair[1].game_configuration.NUMBER_OF_DOTS,
    "attempts_allowed": lambda pair: pair[1].game_configuration.ATTEMPTS_ALLOWED,
    "game_mode": lambda pair: pair[1].game_configuration.GAME_MODE.name,
    "game_started": lambda pair: pair[1].game_state.game_started,
    "winner": lambda pair: pair[1].game_state.winner.name,
    "game_over": lambda pair: pair[1].game_state.game_over,
    "attempts_made": lambda pair: len(pair[1].game_board),
    "guesses": lambda pair: list(pair[1].game_board.guesses),
    "feedbacks": lambda pair: list(pair[1].game_board.feedbacks),
    "code_setter": lambda pair: pair[1].game_entities.CODE_SETTER.__class__.__name__,
    "code_breaker": lambda pair: pair[1].game_entities.CODE_BREAKER.__class__.__name__,
}
valid_keys: Iterable[str] = info_lookup.keys()
