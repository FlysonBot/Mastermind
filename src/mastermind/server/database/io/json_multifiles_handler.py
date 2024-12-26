import os
from typing import Type, TypeVar

from dataclasses_json import DataClassJsonMixin

from mastermind.libs.logs import ServerLogger
from mastermind.server.database.io.io_handler import IOHandler

JsonSerializable = TypeVar("JsonSerializable", bound="DataClassJsonMixin")
logger = ServerLogger("JsonMultiFiles")


class JsonMultiFilesIOHandler(IOHandler[JsonSerializable]):
    """IOHandler for storing data into multiple JSON files in the same directory."""

    def __init__(self, path: str, JSON_constructor: Type[JsonSerializable]) -> None:
        """Initialize the JsonMultiFilesIOHandler.

        Args:
            path (str): The path to the directory where the files will be stored.
        """

        logger.debug(f"Initializing with path: {path}")
        self.path = path
        self.JSON_constructor = JSON_constructor
        os.makedirs(self.path, exist_ok=True)
        logger.info("Initialized successfully")

    def add(self, key: str, value: JsonSerializable) -> None:
        """Create a new file with the given key and JSON-serialize the value.

        Args:
            key (str): The UUID of the item to add.
            value (JsonSerializable): The value of the item to add, will be serialized to JSON.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(os.path.exists(os.path.join(temp_dir, "my_data_class.json")))
            True
        """

        logger.debug(f"Writing to file: {key}.json in {self.path}")

        try:
            with open(os.path.join(self.path, f"{key}.json"), "w") as file:
                file.write(value.to_json())

        except Exception as e:
            self.log_exception(f"Error writing {key}.json", e)

        logger.info(f"Wrote {key}.json to {self.path}")

    def get(self, key: str) -> JsonSerializable:
        """Get the value associated with the given key.

        Args:
            key (str): The UUID of the item to get.

        Returns:
            JsonSerializable: The value associated with the given key.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(io_handler.get("my_data_class"))
            MyDataClass(my_field='Hello, World!')
        """

        logger.debug(f"Reading from file: {key}.json in {self.path}")

        try:
            with open(os.path.join(self.path, f"{key}.json"), "r") as file:
                return self.JSON_constructor.from_json(file.read())

        except FileNotFoundError as e:
            self.log_exception(f"File {key}.json does not exist in {self.path}", e)

        except Exception as e:
            self.log_exception(f"Error reading {key}.json", e)

    def update(self, key: str, value: JsonSerializable) -> None:
        """Update the value associated with the given key.

        Args:
            key (str): The UUID of the item to update.
            value (JsonSerializable): The new value to update the item to.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     io_handler.update("my_data_class", MyDataClass(my_field="Goodbye, World!"))
            ...     print(io_handler.get("my_data_class"))
            MyDataClass(my_field='Goodbye, World!')
        """

        logger.debug(f"Updating file: {key}.json in {self.path}")

        try:
            with open(os.path.join(self.path, f"{key}.json"), "w") as file:
                file.write(value.to_json())

        except FileNotFoundError as e:
            self.log_exception(f"File {key}.json does not exist in {self.path}", e)

        except Exception as e:
            self.log_exception(f"Error updating {key}.json", e)

        logger.info(f"Updated {key}.json in {self.path}")

    def delete(self, key: str) -> None:
        """Delete the item associated with the given key.

        Args:
            key (str): The UUID of the item to delete.

        Raises:
            KeyError: If the key does not exist in the repository.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     io_handler.delete("my_data_class")
            ...     print(io_handler.exists("my_data_class"))
            False
        """

        logger.debug(f"Deleting file: {os.path.join(self.path, f'{key}.json')}")

        try:
            os.remove(os.path.join(self.path, f"{key}.json"))

        except FileNotFoundError as e:
            self.log_exception(f"File {key}.json does not exist in {self.path}", e)

        except Exception as e:
            self.log_exception(f"Error deleting {key}.json", e)

        logger.info(f"Deleted {key}.json from {self.path}")

    def exists(self, key: str) -> bool:
        """Check if the item associated with the given key exists.

        Args:
            key (str): The UUID of the item to check.

        Returns:
            bool: True if the item exists, False otherwise.

        Example:
            >>> from tempfile import TemporaryDirectory
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
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
            >>> from dataclasses_json import dataclass_json
            >>> from dataclasses import dataclass
            >>> @dataclass_json
            ... @dataclass
            ... class MyDataClass:
            ...     my_field: str
            >>> my_data_class = MyDataClass(my_field="Hello, World!")
            >>> with TemporaryDirectory() as temp_dir:
            ...     io_handler = JsonMultiFilesIOHandler(temp_dir, MyDataClass)
            ...     io_handler.add("my_data_class", my_data_class)
            ...     print(io_handler.keys())
            ['my_data_class']
        """
        logger.debug(f"Listing files in directory: {self.path}")
        files = os.listdir(self.path)
        logger.debug(f"Found the following files: {files}")
        return [file[:-5] for file in os.listdir(self.path) if file.endswith(".json")]

    def log_exception(self, log_message: str, exception: Exception):
        logger.error(f"{log_message}: {exception}")
        raise exception
