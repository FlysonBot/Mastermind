import json
import os
from typing import Any, NoReturn, Type, TypeVar

from mastermind.libs.logs import ServerLogger
from mastermind.server.database import converter
from mastermind.server.database.io.io_handler import IOHandler

CattrsSerializable = TypeVar("CattrsSerializable")
logger = ServerLogger("CattrsMultifiles")
JSON = list[Any] | dict[str, Any]


class CattrsMultifilesIOHandler(IOHandler[CattrsSerializable]):
    """IOHandler for storing data into multiple JSON files in the same directory using cattrs to serialize and deserialize."""

    def __init__(self, path: str, data_type: Type[CattrsSerializable]) -> None:
        """Initialize the CattrsMultifilesIOHandler.

        Args:
            path (str): The path to the directory where the files will be stored.
            data_type (Type[CattrsSerializable]): The type of data to be stored, such as a dataclass or attrs class.
        """

        logger.debug(f"Initializing with path: {path}")
        self.path = path
        self.data_type = data_type
        os.makedirs(self.path, exist_ok=True)
        logger.info("Initialized successfully")

    def add(self, key: str, value: CattrsSerializable) -> None:
        """Create a new file with the given key and serialize the value.

        Args:
            key (str): The UUID of the item to add, which will be used as the filename.
            value (CattrsSerializable): The value of the item to add, will be serialized to JSON.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(os.path.exists(os.path.join(temp_dir, "my_data_class.json")))
            True
        """

        logger.debug(f"Writing to file: {key}.json in {self.path}")
        raw_data = _serialize(value)
        _write(self.path, key, raw_data)

    def get(self, key: str) -> CattrsSerializable:
        """Get the value associated with the given key.

        Args:
            key (str): The UUID of the item to get.

        Returns:
            CattrsSerializable: The value associated with the given key.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(io_handler.get("my_data_class"))
            MyDataClass(my_field='Hello, World!')
        """

        logger.debug(f"Reading from file: {key}.json in {self.path}")
        raw_data = _read(self.path, key)
        return _deserialize(raw_data, self.data_type)

    def update(self, key: str, value: CattrsSerializable) -> None:
        """Update the value associated with the given key.

        Args:
            key (str): The UUID of the item to update.
            value (CattrsSerializable): The new value to update the item to.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     io_handler.update("my_data_class", MyDataClass(my_field="Goodbye, World!"))
            ...     print(io_handler.get("my_data_class"))
            MyDataClass(my_field='Goodbye, World!')
        """

        logger.debug(f"Updating file: {key}.json in {self.path} with new data")
        raw_data = _serialize(value)
        _write(self.path, key, raw_data)

    def delete(self, key: str) -> None:
        """Delete the item associated with the given key.

        Args:
            key (str): The UUID of the item to delete.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     io_handler.delete("my_data_class")
            ...     print(io_handler.exists("my_data_class"))
            False
        """

        logger.debug(f"Deleting file: {os.path.join(self.path, f'{key}.json')}")

        try:
            os.remove(os.path.join(self.path, f"{key}.json"))

        except FileNotFoundError as e:
            _log_exception(f"File {key}.json does not exist in {self.path}", e)

        except Exception as e:
            _log_exception(f"Error deleting {key}.json", e)

        logger.info(f"Deleted {key}.json from {self.path}")

    def exists(self, key: str) -> bool:
        """Check if the item associated with the given key exists.

        Args:
            key (str): The UUID of the item to check.

        Returns:
            bool: True if the item exists, False otherwise.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(io_handler.exists("my_data_class"))
            ...     io_handler.delete("my_data_class")
            ...     print(io_handler.exists("my_data_class"))
            True
            False
        """

        logger.debug(
            f"Checking if file exists: {os.path.join(self.path, f'{key}.json')}"
        )
        return os.path.exists(os.path.join(self.path, f"{key}.json"))

    def keys(self) -> list[str]:
        """Get a list of all keys in the repository.

        Returns:
            list[str]: A list of all keys in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses import dataclass
            >>> @dataclass
            ... class MyDataClass:
            ...     my_field: str = "Hello, World!"
            >>> my_data_class = MyDataClass()
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = CattrsMultifilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(io_handler.keys())
            ['my_data_class']
        """
        logger.debug(f"Listing files in directory: {self.path}")
        files = os.listdir(self.path)

        logger.debug(f"Found the following files: {files}")
        return [file[:-5] for file in os.listdir(self.path) if file.endswith(".json")]


def _log_exception(log_message: str, exception: Exception) -> NoReturn:
    logger.error(f"{log_message}: {exception}")
    raise exception


def _serialize(value: object) -> JSON:
    try:
        raw_data: JSON = converter.unstructure(value)

    except Exception as e:
        return _log_exception("Error serializing data", e)

    return raw_data


def _deserialize(
    raw_data: JSON, data_type: Type[CattrsSerializable]
) -> CattrsSerializable:
    try:
        return converter.structure(raw_data, data_type)

    except Exception as e:
        return _log_exception("Error deserializing data", e)


def _write(path: str, key: str, value: JSON) -> None:
    try:
        with open(os.path.join(path, f"{key}.json"), "w") as file:
            json.dump(value, file)

    except Exception as e:
        _log_exception(
            f"Error writing to file: {os.path.join(path, f'{key}.json')}. Data serialized correctly.",
            e,
        )

    logger.info(f"Wrote {key}.json to {path}")


def _read(path: str, key: str) -> JSON:
    try:
        with open(os.path.join(path, f"{key}.json"), "r") as file:
            return json.load(file)  # type: ignore

    except FileNotFoundError as e:
        return _log_exception(f"File {key}.json does not exist in {path}", e)

    except Exception as e:
        return _log_exception(
            f"Error reading from file: {os.path.join(path, f'{key}.json')}", e
        )
