from src.ui.menu.base_menu import BaseMenu


class OptionMenu(BaseMenu):
    """Base class for menus with selectable options."""

    def _print_content(self) -> None:
        for key, value in self.menu.items():
            print(f"({key}) {value}")

    def get_option(self) -> str:
        self.display()
        while True:
            option = input("Select an option: ")
            if option in self.menu:
                return self._process_option(option)
            self.display()
            print("Invalid option. Try again.")

    def _process_option(self, option: str) -> str:
        """Process selected option - can be overridden by subclasses."""
        return self.menu[option]