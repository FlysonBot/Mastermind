from src.ui.menu.base_menu import BaseMenu


class OptionMenu(BaseMenu):
    """
    A concrete implementation of the BaseMenu class for menus with selectable options.

    Provides functionality for displaying the menu options and processing the user's selection.
    """

    def _print_content(self) -> None:
        """
        Prints the menu options.
        """
        for key, value in self.menu.items():
            print(f"({key}) {value}")

    def get_option(self) -> str:
        """
        Displays the menu, prompts the user for an option, and processes the selected option.

        Returns:
            str: The processed option.
        """
        self.display()
        while True:
            option = input("Select an option: ")
            if option in self.menu:
                return self._process_option(option)
            self.display()
            print("Invalid option. Try again.")

    def _process_option(self, option: str) -> str:
        """
        Processes the selected option.

        Args:
            option (str): The selected key from the menu.

        Returns:
            str: The corresponding option name from the menu.
        """
        return self.menu[option]
