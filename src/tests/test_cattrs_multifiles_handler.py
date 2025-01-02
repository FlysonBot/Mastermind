from dataclasses import dataclass

import pytest

from mastermind.server.database.repository import GameRepository


@pytest.fixture
def unexpected_object() -> object:
    class UnexpectedObject:
        some_field: str = "Hello, World!"

    return UnexpectedObject()


@pytest.fixture
def unexpected_serializable() -> object:
    @dataclass
    class UnexpectedSerializable:
        some_field: str = "Hello, World!"

    return UnexpectedSerializable()


def test_delete_nonexistent_file(game_repository: GameRepository) -> None:
    with pytest.raises(FileNotFoundError):
        game_repository.io_handler.delete("nonexistent_file")


def test_repository_unexpected_object(
    game_repository: GameRepository, unexpected_object: object
) -> None:
    with pytest.raises(TypeError):
        game_repository.add(unexpected_object)  # type: ignore


def test_io_handling_unexpected_serializable(
    game_repository: GameRepository, unexpected_serializable: object
) -> None:
    game_repository.io_handler.add("unexpected_serializable", unexpected_serializable)  # type: ignore

    with pytest.raises(Exception):
        game_repository["unexpected_serializable"]  # type: ignore
