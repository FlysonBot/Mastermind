from abc import ABC, abstractmethod


class BaseMenu(ABC):
    """Abstract base class defining core menu behavior."""

    menu = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Menu name. Must be specified by subclasses."""
        pass

    @property
    def width(self) -> int:
        """Calculate menu width dynamically unless overridden."""
        menu_length = (
            max(len(f"({key}) {value}") for key, value in self.menu.items())
            if self.menu
            else 0
        )
        return max(len(self.name) + 8, menu_length)

    def display(self) -> None:
        """Template method defining menu display flow."""
        self._print_header()
        self._print_content()
        self._print_separator()

    def _print_header(self) -> None:
        dashes = "-" * ((self.width - len(self.name) - 1) // 2)
        print(f"\n\n\n{dashes} {self.name} {dashes}")

    @abstractmethod
    def _print_content(self) -> None:
        """Menu content display strategy."""
        pass

    def _print_separator(self) -> None:
        width = ((self.width - len(self.name) - 1) // 2 + 1) * 2 + len(self.name)
        print("-" * width + "\n")
