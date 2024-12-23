from os import path

from appdirs import user_data_dir

from mastermind.database.io import JsonMultiFilesIOHandler
from mastermind.database.models import Game
from mastermind.database.repository import Repository


class GameRepository(Repository[Game]):
    """Repository for storing games."""

    default_path = path.join(user_data_dir("mastermind-ai"), "games")

    def __init__(self, repository_path: str = default_path) -> None:
        """Initialize the GameRepository."""
        super().__init__(
            JsonMultiFilesIOHandler(
                repository_path,
                Game,
            )
        )
