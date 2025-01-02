from os import path

from appdirs import user_data_dir

from ..io import CattrsMultifilesIOHandler
from ..models import Game
from .repository import Repository


class GameRepository(Repository[Game]):
    """Repository for storing games."""

    default_path: str = path.join(user_data_dir("mastermind-ai"), "games")

    def __init__(self, repository_path: str = default_path) -> None:
        """Initialize the GameRepository."""
        super().__init__(
            CattrsMultifilesIOHandler(
                repository_path,
                Game,
            )
        )
