import os
from typing import Type, TypeVar

from dataclasses_json import DataClassJsonMixin

from mastermind.server.database.io.io_handler import IOHandler

JsonSerializable = TypeVar("JsonSerializable", bound="DataClassJsonMixin")


class JsonMultiFilesIOHandler(IOHandler[JsonSerializable]):
    """IOHandler for storing data into multiple JSON files in the same directory."""

    def __init__(self, path: str, JSON_constructor: Type[JsonSerializable]) -> None:
        """Initialize the JsonMultiFilesIOHandler.

        Args:
            path (str): The path to the directory where the files will be stored.
        """

        self.path = path
        self.JSON_constructor = JSON_constructor
        os.makedirs(self.path, exist_ok=True)

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

        with open(os.path.join(self.path, f"{key}.json"), "w") as file:
            file.write(value.to_json())  # type: ignore

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

        with open(os.path.join(self.path, f"{key}.json"), "r") as file:
            return self.JSON_constructor.from_json(file.read())  # type: ignore

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

        with open(os.path.join(self.path, f"{key}.json"), "w") as file:
            file.write(value.to_json())  # type: ignore

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

        os.remove(os.path.join(self.path, f"{key}.json"))

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

        return [file[:-5] for file in os.listdir(self.path) if file.endswith(".json")]
