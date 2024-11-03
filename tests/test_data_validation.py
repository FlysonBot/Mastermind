import unittest
from ..data_validation import *

class GameSettings(BaseModel):
    """Class to manage game settings with validated attributes."""
    
    def __init__(self):
        # Initialize validated attributes
        self.constant_value = Constant(42)
        self.number_of_dots = NumberOfDots(5)
        self.number_of_colors = NumberOfColors(3)

class TestGameSettings(unittest.TestCase):
    
    def setUp(self):
        """Create a GameSettings instance for testing."""
        self.settings = GameSettings()

    def test_constant_initialization(self):
        """Test initialization of a constant value."""
        self.assertEqual(self.settings.constant_value, 42)

    def test_constant_modification_error(self):
        """Test that modifying a constant raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.constant_value = 50  # Should raise an error

    def test_valid_number_of_dots(self):
        """Test setting a valid number of dots."""
        self.settings.number_of_dots = 10
        self.assertEqual(self.settings.number_of_dots, 10)

    def test_invalid_number_of_dots_negative(self):
        """Test that setting a negative number of dots raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_dots = -1  # Should raise an error

    def test_invalid_number_of_dots_non_integer(self):
        """Test that setting a non-integer number of dots raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_dots = 2.5  # Should raise an error

    def test_valid_number_of_colors(self):
        """Test setting a valid number of colors."""
        self.settings.number_of_colors = 5
        self.assertEqual(self.settings.number_of_colors, 5)

    def test_invalid_number_of_colors_too_few(self):
        """Test that setting too few colors raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_colors = 1  # Should raise an error

    def test_invalid_number_of_colors_non_integer(self):
        """Test that setting a non-integer number of colors raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_colors = "three"  # Should raise an error


if __name__ == '__main__':
    unittest.main()

