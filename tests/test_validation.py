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

    def test_constant(self):
        self.assertEqual(self.settings.CONSTANT_VALUE, 42)
        
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.CONSTANT_VALUE = 50  # Should raise an error

    def test_number_of_dots(self):
        self.settings.number_of_dots = 10
        self.assertEqual(self.settings.number_of_dots, 10)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_dots = -1  # Should raise an error
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_dots = 2.5  # Should raise an error

    def test_number_of_colors(self):
        self.settings.number_of_colors = 5
        self.assertEqual(self.settings.number_of_colors, 5)
        
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_colors = 1  # Should raise an error
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_colors = "three"  # Should raise an error
    
    def test_chain_validation(self):
        self.settings.NUMBER_OF_COLORS = 3  # Chaining
        self.assertEqual(self.settings.NUMBER_OF_COLORS, 3)
        
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

