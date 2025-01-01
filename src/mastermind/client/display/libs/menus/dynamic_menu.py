from abc import ABC, abstractmethod
from dataclasses import field

from mastermind.client.display.libs.menus.back import back
from mastermind.client.display.libs.menus.menu_config import MenuConfig
from mastermind.client.display.libs.menus.menu_option import MenuOption, MenuOptions


class DynamicMenu(ABC):
    config: MenuConfig
    options: MenuOptions = field(default_factory=list)

    @classmethod
    @abstractmethod
    def reconstruct_menu(cls) -> None:
        pass

    @classmethod
    def add_option(cls, option: MenuOption) -> None:
        cls.options.append(option)

    @classmethod
    def get_selections(cls) -> MenuOptions:  # in case of multiple selections
        cls.reconstruct_menu()
        cls.config.logger.debug(f"Menu options: {cls.options}")

        selection: MenuOptions = cls.config.menu_adapter(
            cls.config.title, cls.options, cls.config.display_mode, **cls.config.kwargs
        ).get_selections()

        cls.config.logger.debug(f"Selections: {selection}")
        return selection

    @classmethod
    def activate(cls) -> None:
        cls.config.logger.debug(
            f"Activating menu: {cls.__name__}. Stay in menu: {cls.config.stay_in_menu}"
        )
        while cls.get_selections()[0].action() is not back and cls.config.stay_in_menu:
            pass
