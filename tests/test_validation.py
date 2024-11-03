import unittest
from ..validation import *

class GameSettings(BaseModel):
    """Class to manage game settings with validated attributes."""
    
    def __init__(self):
        # Initialize attributes (validation models will be automatically applied)
        self.CONSTANT_VALUE = 42
        self.number_of_dots = 5
        self.number_of_colors = 3

class TestGameSettings(unittest.TestCase):
    
    def setUp(self):
        """Create a GameSettings instance for testing."""
        self.settings = GameSettings()

    def test_constant_initialization(self):
        """Test initialization of a constant value."""
        self.assertEqual(self.settings.CONSTANT_VALUE, 42)

    def test_constant_modification_error(self):
        """Test that modifying a constant raises an error."""
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.CONSTANT_VALUE = 50  # Should raise an error

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
    
    def test_valid_chain_validation(self):
        """Test chaining constant and number of colors."""
        del self.settings.number_of_colors  # Delete the original one first
        self.settings.NUMBER_OF_COLORS = 3  # Chaining
        self.assertEqual(self.settings.NUMBER_OF_COLORS, 3)
    
    def test_invalid_chain_validation(self):
        """Test chaining constant and invalid number of dots raises error."""
        del self.settings.number_of_dots  # Delete the original one first
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.NUMBER_OF_DOTS = -1  # Should raise an error
    
    def test_unvalidated_type(self):
        """Test handling normal unvalidated type."""
        self.settings.integer = 5  # normal int type
        self.assertEqual(self.settings.integer, 5)
        self.settings.float = 9.8  # normal float type
        self.assertEqual(self.settings.float, 9.8)
        self.settings.float = 1.2  # attempt to modify float
        self.assertEqual(self.settings.float, 1.2)
        self.settings.list = [1, 2]  # normal list
        self.assertEqual(self.settings.list, [1, 2])


if __name__ == '__main__':
    unittest.main()

