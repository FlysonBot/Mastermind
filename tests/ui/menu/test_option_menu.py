import unittest
from unittest.mock import call, patch

from mastermind.ui.menu.option_menu import OptionMenu


class TestOptionMenu(unittest.TestCase):
    class ConcreteOptionMenu(OptionMenu):
        name = "Options"
        menu = {
            "1": "Option 1",
            "2": "Option 2",
            "q": "Quit",
        }

    def setUp(self):
        self.option_menu = self.ConcreteOptionMenu()

    @patch("builtins.print")
    def test_print_content(self, mock_print):
        self.option_menu._print_content()
        mock_print.assert_has_calls(
            [call("(1) Option 1"), call("(2) Option 2"), call("(q) Quit")]
        )

    @patch("builtins.input", side_effect=["2"])
    @patch.object(OptionMenu, "display")
    def test_get_option(self, mock_display, mock_input):
        self.assertEqual(self.option_menu.get_option(), "Option 2")
        mock_display.assert_called_once()
        mock_input.assert_has_calls([call("Select an option: ")])

    @patch.object(OptionMenu, "_print_content")
    def test_get_option_invalid(self, mock_print_content):
        with (
            patch("builtins.input", side_effect=["invalid", "q"]),
            patch("builtins.print") as mock_print,
        ):
            self.assertEqual(self.option_menu.get_option(), "Quit")
            mock_print.assert_has_calls([call("Invalid option. Try again.")])
            mock_print_content.assert_called()

    def test_process_option(self):
        self.assertEqual(self.option_menu._process_option("1"), "Option 1")
        self.assertEqual(self.option_menu._process_option("2"), "Option 2")
        self.assertEqual(self.option_menu._process_option("q"), "Quit")


if __name__ == "__main__":
    unittest.main()
