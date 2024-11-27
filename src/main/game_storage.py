from src.storage.user_data import UserDataManager


def retrieve_stored_games():
    """Retrieve all stored games"""
    saved_games = UserDataManager().saved_games
    return saved_games or []


def list_continuable_games_index(stored_games):
    """Return a list of indexes of the stored games that can be continued."""
    if not stored_games:  # no games
        return []
    return [
        index for index, game in enumerate(stored_games) if game["win_status"] is None
    ]


def list_continuable_games(stored_games):
    """Return a list of the stored games that can be continued."""
    if not stored_games:  # no games
        return []
    return [game for game in stored_games if game["win_status"] is None]
