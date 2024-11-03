import unittest
from ..validation import *

class GameSettings(BaseModel):
    """Class to manage game settings with validated attributes."""
    
    def __init__(self):
        # Initialize attributes (validation models will be automatically applied)
        self.CONSTANT_VALUE = 42
        self.number_of_dots = 5
        self.number_of_colors = 3
        self.number_of_guesses_made = 0
        self.maximum_attempts = 10
        self.game_mode = 'HvAI'
        self.secret_code = SecretCode((1, 2, 3), number_of_dots=5, number_of_colors=3)
        self.boolean_flag = None
        self.true_fuse = True
        self.false_fuse = False

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

    def test_number_of_guesses_made(self):
        self.settings.number_of_guesses_made = 3
        self.assertEqual(self.settings.number_of_guesses_made, 3)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_guesses_made = -1  # Should raise error for negative
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.number_of_guesses_made = "five"  # Non-integer string

    def test_maximum_attempts(self):
        self.settings.maximum_attempts = 5
        self.assertEqual(self.settings.maximum_attempts, 5)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.maximum_attempts = 0  # Should raise error for less than 1
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.maximum_attempts = "ten"  # Non-integer string

    def test_game_mode(self):
        self.settings.game_mode = 'AIvAI'
        self.assertEqual(self.settings.game_mode, 'AIvAI')

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.game_mode = 'QvQ'  # Invalid game mode
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.game_mode = ''  # Empty string

    def test_secret_code(self):
        self.settings.secret_code = (1, 2, 3)
        self.assertEqual(self.settings.secret_code, (1, 2, 3))

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.secret_code = (1, 2)  # Incorrect length
        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.secret_code = (1, 4, 3)  # Value out of range

    def test_boolean_flag(self):
        self.settings.boolean_flag = True
        self.assertTrue(self.settings.boolean_flag)

        self.settings.boolean_flag = False
        self.assertFalse(self.settings.boolean_flag)

        self.settings.boolean_flag = None
        self.assertIsNone(self.settings.boolean_flag)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.boolean_flag = "True"  # Should raise error for non-boolean

    def test_true_fuse(self):
        self.assertTrue(self.settings.true_fuse)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.true_fuse = False  # Cannot set TrueFuse to False

    def test_false_fuse(self):
        self.assertFalse(self.settings.false_fuse)

        with self.assertRaises(ValidatedData.ValidationError):
            self.settings.false_fuse = True  # Cannot set FalseFuse to True


if __name__ == '__main__':
    unittest.main()

