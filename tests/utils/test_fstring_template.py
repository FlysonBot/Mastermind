import unittest

from src.utils.fstring_template import FStringTemplate


class TestFStringTemplate(unittest.TestCase):
    """Test suite for the FStringTemplate class"""

    def test_init(self):
        """Test that FStringTemplate can be initialized with a template string"""
        template = FStringTemplate("Hello, {name}!")
        self.assertEqual(template.template, "Hello, {name}!")

    def test_eval_with_valid_kwargs(self):
        """Test that FStringTemplate can format a string with valid keyword arguments"""
        template = FStringTemplate("Hello, {name}! You are {age} years old.")
        formatted_string = template.eval(name="Alice", age=30)
        self.assertEqual(formatted_string, "Hello, Alice! You are 30 years old.")

    def test_eval_with_missing_kwargs(self):
        """Test that FStringTemplate raises an error when a required keyword argument is missing"""
        template = FStringTemplate("Hello, {name}! You are {age} years old.")
        with self.assertRaises(KeyError) as context:
            template.eval(name="Alice")
        self.assertEqual(str(context.exception), "'age'")

    def test_eval_with_extra_kwargs(self):
        """Test that FStringTemplate ignores extra keyword arguments"""
        template = FStringTemplate("Hello, {name}! You are {age} years old.")
        formatted_string = template.eval(name="Alice", age=30, city="New York")
        self.assertEqual(formatted_string, "Hello, Alice! You are 30 years old.")


if __name__ == "__main__":
    unittest.main()
