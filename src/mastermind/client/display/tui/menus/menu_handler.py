from clear_screen import clear  # type: ignore

from mastermind.client.display.libs.menus import MenuAdapter
from mastermind.client.display.libs.menus.display_mode import DisplayMode
from mastermind.client.display.libs.menus.menu_option import MenuOptions


class MenuHandler(MenuAdapter):
    def get_selections(self) -> MenuOptions:
        self.print_menu()
        return self._get_selections()

    def print_menu(self) -> None:
        body = _generate_body(self.menu_options, self.display_mode)
        width = _calculate_width(self.title, body)

        clear()
        print(_generate_header(self.title, width))
        for line in body:
            print(line)
        print(_generate_footer(self.title, width))

    def _get_selections(self) -> MenuOptions:
        keys = list(map(lambda option: option.value, self.menu_options))
        choice = None
        input_hint = self.kwargs.get("input_hint", "Enter your choice: ")

        while (choice := input(input_hint)) not in keys:
            clear()
            self.print_menu()
            print("Invalid choice. Please try again.")

        clear()
        return [self.menu_options[keys.index(choice)]]


def _generate_header(title: str, width: int) -> str:
    margin_length = (width - text_width(title)) // 2
    return f"\n{'=' * margin_length} {title} {'=' * margin_length}"


def _generate_footer(title: str, width: int) -> str:
    return f"{'=' * (text_width(_generate_header(title, width))-1)}\n"


def _generate_body(menu_options: MenuOptions, display_mode: DisplayMode) -> list[str]:
    if display_mode == DisplayMode.TITLE_ONLY:
        return [f" {option.title}" for option in menu_options]

    if display_mode == DisplayMode.BOTH:
        return [f" ({option.value}) {option.title}" for option in menu_options]

    raise ValueError(f"Unsupported display mode: {display_mode}")


def _calculate_width(title: str, body: list[str]) -> int:
    return max(text_width(title), max(map(text_width, body)))


def text_width(text: str) -> int:
    """Calculate the width of a string in characters, taking into account Chinese characters."""
    return sum(2 if "\u4e00" <= char <= "\u9fff" else 1 for char in text)