from os import path

from appdirs import user_data_dir  # type: ignore

from mastermind.core.models.game import Game
from mastermind.libs.storage.json_multifiles_io_handler import JsonMultiFilesIOHandler
from mastermind.libs.storage.repository import Repository


class GameRepository(Repository[Game]):
    """Repository for storing games."""

    default_path = path.join(user_data_dir("mastermind-ai"), "games")  # type: ignore

    def __init__(self, repository_path: str = default_path) -> None:
        """Initialize the GameRepository."""
        super().__init__(
            JsonMultiFilesIOHandler(
                repository_path,
                Game,
            )
        )
