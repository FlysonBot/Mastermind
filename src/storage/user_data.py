import os
import pickle
from typing import Any


class UserDataManager:
    """
    Manages user data using a singleton pattern.

    The UserDataManager class stores user data in a dictionary and persists it to a file on the file system using the pickle module.

    The class is implemented as a singleton, ensuring that there is only one instance of the UserDataManager class.
    """

    _instance = None  # Class-level attribute for the singleton instance
    _data = {}  # Dictionary to hold user data
    _file_path = "data/userdata.config"  # Path to the user data file

    def __new__(cls) -> "UserDataManager":
        """
        Returns the singleton instance of the UserDataManager class.

        If the instance does not exist, it is created and the data is loaded from the file.
        """

        if cls._instance is None:
            cls._instance = super(UserDataManager, cls).__new__(cls)
            cls._instance._load_data()  # Load data on instantiation
        return cls._instance

    @classmethod
    def _ensure_directory_exists(cls) -> None:
        """This method creates the directory if it does not already exist."""
        if directory := os.path.dirname(cls._file_path):
            os.makedirs(directory, exist_ok=True)
        else:
            raise ValueError("cls._file_path must include a directory component")

    def _load_data(self) -> None:
        """
        Loads the user data from the file.

        If the file does not exist, an empty dictionary is used as the initial user data.
        """

        self._ensure_directory_exists()  # Ensure the directory is created
        try:
            with open(self._file_path, "rb") as file:
                self._data = pickle.load(file)
                return

        except FileNotFoundError:  # on first run
            self._data = {}
            return

        except EOFError as e:
            print("There seems to be an issue loading the data.")
            print(e)
            print("\nIf this issue persists, consider deleting the stored data.")
        except ModuleNotFoundError as e:
            print(
                "There is an error loading the stored data. Your data or app version might not match."
            )
            print(e)
            print("\nTo resolve this issue, consider deleting the stored data.")
        except Exception as e:
            print("An unexpected error occurred while loading the data.")
            print(e)
            print("\nIf this issue persists, consider deleting the stored data.")

        if not prompt_delete_data():
            raise Exception("Data could not be loaded.")

    def save_data(self) -> None:
        """Saves the user data to the file."""
        self._ensure_directory_exists()  # Ensure the directory is created
        with open(self._file_path, "wb") as file:
            pickle.dump(self._data, file)

    def clear_all(self) -> None:
        """Clears all the user data and saves the changes."""
        self._data = {}
        self.save_data()

    def _retrieve_item(self, key: str) -> Any:
        """
        Retrieves the value associated with the given key, or None if the key does not exist.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Any: The value associated with the key, or None if the key does not exist.
        """

        return self._data[key] if key in self._data else None

    def _modify_item(self, key: str, value: Any) -> None:
        """
        Modify the value associated with the given key in the internal dictionary.
        If the key is one of the instance attribute, it modify that instead.
        After modifying the internal dictionary, it saves the changes to the file.

        Args:
            key (str): The key to modify the value for.
            value (Any): The new value to associate with the key.
        """

        if key in {
            "_instance",
            "_data",
            "_file_path",
        }:  # Prevent overriding class attributes
            super().__setattr__(key, value)
        else:
            self._data[key] = value
            self.save_data()

    def __getattr__(self, key: str) -> Any:
        """Retrieves the value associated with the given key."""
        return self._retrieve_item(key)

    def __getitem__(self, key: str) -> Any:
        """Retrieves the value associated with the given key."""
        return self._retrieve_item(key)

    def __setattr__(self, key: str, value: Any) -> None:
        """Modifies the value associated with the given key, and saves the changes."""
        self._modify_item(key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        """Modifies the value associated with the given key, and saves the changes."""
        self._modify_item(key, value)

    def __contains__(self, key: str) -> bool:
        """Checks if the given key exists in the user data."""
        return key in self._data


def prompt_delete_data() -> bool:
    decision = input("Do you want to delete the stored data? (y/n): ")
    if decision.lower() != "y":
        return False
    UserDataManager().clear_all()
    print("Data deleted successfully.")
    return True
