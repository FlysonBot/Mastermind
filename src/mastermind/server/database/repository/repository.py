from abc import ABC
from typing import Any, Dict, Generator, Generic, TypeVar

from shortuuid import ShortUUID

from ..io import IOHandler

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Abstract base class for repository pattern. It is designed with an interface similar to dictionary."""

    def __init__(self, io_handler: IOHandler[T]) -> None:
        """Initialize the repository.

        Args:
            io_handler (IOHandler[T]): The IO handler to use for the repository.
        """

        self.data: Dict[str, T] = {}
        self.io_handler: IOHandler[T] = io_handler

    def __contains__(self, name: str) -> bool:
        """Check if an item exists in the repository.

        Args:
            name (str): The name of the item to check.

        Returns:
            bool: True if the item exists, False otherwise.
        """

        return name in self.data or self.io_handler.exists(name)

    def add(self, value: T) -> str:
        """Add a new item to the repository and return its UUID.

        Args:
            value (T): The value of the item to add.

        Returns:
            str: The UUID of the added item.
        """

        uuid: str = ShortUUID().random(length=6)

        if uuid in self:
            return self.add(value)  # try again

        self.io_handler.add(uuid, value)
        self.data[uuid] = value
        return uuid

    def __delitem__(self, name: str) -> None:
        """Delete an item from the repository.

        Args:
            name (str): The name of the item to delete.

        Raises:
            KeyError: If the item does not exist in the repository.
        """

        if name not in self:
            raise KeyError(name)

        if self.io_handler.exists(name):
            self.io_handler.delete(name)

        if name in self:
            del self.data[name]

    def __getitem__(self, name: str) -> T:
        """Get an item from the repository.

        Args:
            name (str): The name of the item to get.

        Returns:
            T: The value of the item.

        Raises:
            KeyError: If the item does not exist in the repository.
        """

        if name in self.data:
            return self.data[name]

        if self.io_handler.exists(name):
            value: T = self.io_handler.get(name)
            self.data[name] = value
            return value

        raise KeyError(name)

    def __setitem__(self, name: str, value: T) -> None:
        """Update an item in the repository.

        Args:
            name (str): The name of the item to update.
            value (T): The new value of the item.

        Raises:
            KeyError: If the item does not exist in the repository.
        """

        if name not in self:
            raise KeyError(name)

        if self.io_handler.exists(name):
            self.io_handler.update(name, value)

        self.data[name] = value

    def __iter__(self) -> Generator[Any, None, None]:
        """Iterate over the items in the repository.

        Yields:
            Any: The next item in the repository.
        """

        for name in self.io_handler.keys():
            yield (name, self[name])

    def __next__(self) -> T:
        """Get the next item in the repository.

        Returns:
            T: The next item in the repository.
        """

        return next(iter(self))

    def __len__(self) -> int:
        """Get the number of items in the repository.

        Returns:
            int: The number of items in the repository.
        """

        return len(self.io_handler.keys())
