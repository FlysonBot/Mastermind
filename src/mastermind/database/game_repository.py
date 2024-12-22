from os import path

from appdirs import user_data_dir  # type: ignore

from mastermind.database.libs import (
    JsonMultiFilesIOHandler,
    Repository,
)
from mastermind.database.models import Game


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
