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
        return max((len(key) for key in self.menu.keys()), default=len(self.name) + 8)

    def display(self) -> None:
        """Template method defining menu display flow."""
        self._print_header()
        self._print_content()
        self._print_separator()

    def _print_header(self) -> None:
        width = (self.width - len(self.name) - 1) // 2
        print(f"\n\n\n{'-' * width} {self.name} {'-' * width}")

    @abstractmethod
    def _print_content(self) -> None:
        """Menu content display strategy."""
        pass

    def _print_separator(self) -> None:
        width = ((self.width - len(self.name) - 1) // 2 + 1) * 2 + len(self.name)
        print("-" * width + "\n")
