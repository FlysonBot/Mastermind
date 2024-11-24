import io
import unittest
from unittest.mock import patch

import pandas as pd

from src.utils.render_dataframe import (
    _calculate_column_widths,
    _calculate_index_width,
    _prepare_header,
    _print_row,
    render_dataframe,
)


class TestRenderDataframe(unittest.TestCase):
    """Test suite for the render_dataframe function and related utility functions"""

    def test_calculate_index_width(self):
        """Test that _calculate_index_width calculates the width correctly"""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=[10, 100, 1000])
        self.assertEqual(_calculate_index_width(df), 4)

        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=["a", "bb", "ccc"])
        self.assertEqual(_calculate_index_width(df), 3)

        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=[10.0, 100.0, 1000.0])
        self.assertEqual(_calculate_index_width(df), 6)

    def test_calculate_column_widths(self):
        """Test that _calculate_column_widths calculates the widths correctly"""
        df = pd.DataFrame({"A": [1, 2, 3], "B": ["abc", "def", "ghi"]})
        self.assertEqual(_calculate_column_widths(df), [1, 3])

        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        self.assertEqual(_calculate_column_widths(df), [1, 1])

        df = pd.DataFrame({"A": [1.0, 2.0, 3.0], "B": [4.0, 5.0, 6.0]})
        self.assertEqual(_calculate_column_widths(df), [3, 3])

    def test_prepare_header(self):
        """Test that _prepare_header prepares the header correctly"""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        self.assertEqual(_prepare_header(df), [" ", "A", "B"])

        df = pd.DataFrame(
            {"A": [1, 2, 3], "B": [4, 5, 6]}, index=pd.Index([10, 20, 30], name="Index")
        )
        self.assertEqual(_prepare_header(df), ["Index", "A", "B"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_row(self, mock_stdout):
        """Test that _print_row prints the row correctly"""
        _print_row(["Index", "A", "B"], [5, 5, 5])
        self.assertEqual(mock_stdout.getvalue(), "Index A     B    \n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_render_dataframe(self, mock_stdout):
        """Test that render_dataframe renders the DataFrame correctly"""
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]}, index=[10, 20, 30])
        render_dataframe(df)
        expected_output = "   A B\n10 1 4\n20 2 5\n30 3 6\n"
        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
