import io
import unittest
from unittest.mock import patch

from src.ui.menu.base_menu import BaseMenu


class TestBaseMenu(BaseMenu):
    """Test implementation of the BaseMenu class"""

    @property
    def name(self) -> str:
        return "Test Menu"

    def _print_content(self) -> None:
        for key, value in self.menu.items():
            print(f"{key}: {value}")


class TestBaseMenuClass(unittest.TestCase):
    """Test suite for the BaseMenu class"""

    def setUp(self):
        self.base_menu = TestBaseMenu()
        self.base_menu.menu = {
            "Option 1": "Description 1",
            "Option 2": "Description 2",
            "Option 3": "Description 3",
        }

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_display(self, mock_stdout):
        """Test that the display method prints the correct output"""
        self.base_menu.display()
        expected_output = "\n\n\n------ Test Menu ------\nOption 1: Description 1\nOption 2: Description 2\nOption 3: Description 3\n-----------------------\n\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_width(self):
        """Test that the width property returns the correct value"""
        self.assertEqual(self.base_menu.width, 23)


if __name__ == "__main__":
    unittest.main()
