from abc import ABC, abstractmethod


class BaseMenu(ABC):
    """
    The abstract base class for all menu-based user interfaces.

    Provides common functionality for displaying menus, including printing headers, content, and separators.
    """

    menu = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Returns the name of the menu.

        This is an abstract property that must be implemented by subclasses.
        """
        pass

    @property
    def width(self) -> int:
        """
        Returns the width of the menu, based on the maximum length of the menu items.
        """
        return max((len(key) for key in self.menu.keys()), default=len(self.name) + 8)

    def display(self) -> None:
        """
        Displays the menu by printing the header, content, and separator.
        """
        self._print_header()
        self._print_content()
        self._print_separator()

    def _print_header(self) -> None:
        """
        Prints the header of the menu, centered around the menu name.
        """
        width = (self.width - len(self.name) - 1) // 2
        print(f"\n\n\n{'-' * width} {self.name} {'-' * width}")

    @abstractmethod
    def _print_content(self) -> None:
        """
        Prints the content of the menu.

        This is an abstract method that must be implemented by subclasses.
        """
        pass

    def _print_separator(self) -> None:
        """
        Prints a separator line for the menu.
        """
        width = ((self.width - len(self.name) - 1) // 2 + 1) * 2 + len(self.name)
        print("-" * width + "\n")
