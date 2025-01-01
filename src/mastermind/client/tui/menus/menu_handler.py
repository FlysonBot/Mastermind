from typing import Any

from clear_screen import clear  # type: ignore

from mastermind.client.languages import global_localization
from mastermind.libs.menus import DisplayMode, MenuAdapter, MenuOptions

menu_handler = global_localization.menu.menu_handler


class MenuHandler(MenuAdapter):
    def get_selections(self) -> MenuOptions:
        self.print_menu()
        return self._get_selections()

    def print_menu(self) -> None:
        body: list[str] = _generate_body(self.menu_options, self.display_mode)
        width: int = _calculate_width(self.title, body)

        clear()
        print(_generate_header(self.title, width))
        for line in body:
            print(line)
        print(_generate_footer(self.title, width))

    def _get_selections(self) -> MenuOptions:
        keys = list(map(lambda option: option.value, self.menu_options))
        choice = None
        input_hint: dict[Any, Any] = self.kwargs.get(
            "input_hint", menu_handler.default_input_hint
        )

        while (choice := input(input_hint)) not in keys:
            clear()
            self.print_menu()
            menu_handler.invalid_choice()

        clear()
        return [self.menu_options[keys.index(choice)]]  # type: ignore


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

    raise ValueError(menu_handler.unsupported_display_mode(display_mode=display_mode))


def _calculate_width(title: str, body: list[str]) -> int:
    return max(text_width(title), max(map(text_width, body)))


def text_width(text: str) -> int:
    """Calculate the width of a string in characters, taking into account Chinese characters."""
    return sum(2 if "\u4e00" <= char <= "\u9fff" else 1 for char in text)
