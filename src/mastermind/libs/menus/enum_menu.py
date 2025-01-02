from abc import abstractmethod
from enum import Enum
from typing import Optional

from .back import back
from .menu_config import MenuConfig
from .menu_option import MenuOptions


class EnumMenu(Enum):
    """A type of menu generated from an enum class, where the value of each member is a MenuOption."""

    @classmethod
    @abstractmethod
    def config(cls) -> MenuConfig:
        """Return the menu configuration. This avoid specifying configuration as a member of enum."""
        pass

    @classmethod
    def list_options(cls) -> MenuOptions:
        """Return a list of menu options by listing the value of each member."""
        return [member.value for member in cls]

    @classmethod
    def get_selections(cls) -> MenuOptions:
        """Repeatedly prompt the user to select an option from the menu until a valid selection is made.

        Returns:
            MenuOptions: A list of selected menu options (in case of multiple selections).
        """
        config: MenuConfig = cls.config()
        selection: MenuOptions = config.menu_adapter(
            config.title, cls.list_options(), config.display_mode
        ).get_selections()

        cls.config().logger.debug(f"Selections: {selection}")

        return selection

    @classmethod
    def activate(cls, stay_in_menu: Optional[bool] = False) -> None:
        """Switch to the menu to display and handle user selections."""
        stay_in_menu = stay_in_menu or cls.config().stay_in_menu

        cls.config().logger.debug(
            f"Activating menu: {cls.__name__}. Stay in menu: {stay_in_menu}"
        )

        while (
            cls.get_selections()[0].action() is not back and cls.config().stay_in_menu
        ):
            pass
