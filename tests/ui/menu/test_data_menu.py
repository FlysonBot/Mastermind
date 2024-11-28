import unittest
from typing import Any
from unittest.mock import call, patch

from mastermind.ui.menu.data_menu import DataDisplayMenu


class TestDataDisplayMenu(unittest.TestCase):
    class ConcreteDataDisplayMenu(DataDisplayMenu):
        name = "Data Menu"
        _fetch_data = None
        _render_data = None
        _empty_message = None

    def setUp(self):
        self.data_menu = self.ConcreteDataDisplayMenu()

    @patch.object(ConcreteDataDisplayMenu, "_fetch_data", return_value="test data")
    @patch.object(ConcreteDataDisplayMenu, "_render_data")
    def test_print_content_with_data(self, mock_render_data, mock_fetch_data):
        with patch("builtins.print") as mock_print:
            self.data_menu._print_content()
            mock_fetch_data.assert_called()
            mock_render_data.assert_called_with("test data")
            mock_print.assert_not_called()

    @patch.object(ConcreteDataDisplayMenu, "_fetch_data", return_value=None)
    @patch.object(ConcreteDataDisplayMenu, "_render_data")
    @patch.object(
        ConcreteDataDisplayMenu, "_empty_message", return_value="No data available"
    )
    def test_print_content_without_data(
        self, mock_empty_message, mock_render_data, mock_fetch_data
    ):
        with patch("builtins.print") as mock_print:
            self.data_menu._print_content()
            mock_fetch_data.assert_called()
            mock_render_data.assert_not_called()
            mock_print.assert_called_with("No data available")

    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            DataDisplayMenu()

        def render_data(data: Any) -> None:
            for item in data:
                print(item)

        self.data_menu._fetch_data = lambda: [1, 2, 3, 4]
        self.data_menu._render_data = render_data

        with patch("builtins.print") as mock_print:
            self.data_menu._print_content()
            mock_print.assert_has_calls([call(1), call(2), call(3), call(4)])


if __name__ == "__main__":
    unittest.main()
