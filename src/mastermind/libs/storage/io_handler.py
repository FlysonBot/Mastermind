from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IOHandler(ABC, Generic[T]):
    """Abstract base class for handling IO operations in a repository.

    This class defines the interface for handling IO operations in a repository, such as adding, getting, and updating items. It provides a common interface for different implementations of how the repository is stored.
    """

    @abstractmethod
    def add(self, key: str, value: T) -> None:
        """Add a new item to the repository.

        Args:
            key (str): The key of the item to add.
            value (T): The value of the item to add.
        """

    @abstractmethod
    def get(self, key: str) -> T:
        """Get an item from the repository.

        Args:
            key (str): The key of the item to get.

        Returns:
            T: The value of the item.

        Raises:
            KeyError: If the key does not exist in the repository.
        """

    @abstractmethod
    def update(self, key: str, value: T) -> None:
        """Update an item in the repository.

        Args:
            key (str): The key of the item to update.
            value (T): The new value of the item.

        Raises:
            KeyError: If the key does not exist in the repository.
        """

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete an item from the repository.

        Args:
            key (str): The key of the item to delete.

        Raises:
            KeyError: If the key does not exist in the repository.
        """

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if an item exists in the repository.

        Args:
            key (str): The key of the item to check.

        Returns:
            bool: True if the item exists, False otherwise.
        """

    @abstractmethod
    def keys(self) -> list[str]:
        """Get a list of all keys in the repository.

        Returns:
            list[str]: A list of all keys in the repository.
        """
