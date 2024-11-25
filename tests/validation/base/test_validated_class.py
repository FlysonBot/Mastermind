import unittest

from src.validation.base.exceptions import InvalidModificationError
from src.validation.base.semi_mutable import TrueFuse
from src.validation.base.validated_class import ValidatedClass


class TestValidatedClass(unittest.TestCase):
    """Test suite for the ValidatedClass"""

    class MyValidatedTrueFuseClass(ValidatedClass):
        my_bool: TrueFuse

        def __init__(self, value: bool):
            self.my_bool = TrueFuse(value)

    class MyValidatedIntClass(ValidatedClass):
        my_int: int

        def __init__(self, value: int):
            self.my_int = value

    def test_get_attribute_with_state_validator(self):
        """Test that ValidatedClass automatically unwraps StateValidator attributes"""


        obj = self.MyValidatedTrueFuseClass(True)
        self.assertTrue(obj.my_bool)

    def test_set_attribute_with_state_validator(self):
        """Test that ValidatedClass automatically validates modifications to StateValidator attributes"""

        obj = self.MyValidatedTrueFuseClass(True)
        obj.my_bool = True
        self.assertTrue(obj.my_bool)

        with self.assertRaises(InvalidModificationError) as context:
            obj.my_bool = False
        self.assertEqual(
            str(context.exception), "TrueFuse can only be modified to True"
        )

    def test_set_attribute_without_state_validator(self):
        """Test that ValidatedClass behaves normally for non-StateValidator attributes"""

        # sourcery skip: class-extract-method
        obj = self.MyValidatedIntClass(42)
        obj.my_int = 10
        self.assertEqual(obj.my_int, 10)

    def test_set_new_attribute(self):
        """Test that ValidatedClass can set new attributes normally"""

        obj = self.MyValidatedIntClass(0)
        obj.new_attr = 42
        self.assertEqual(obj.new_attr, 42)


if __name__ == "__main__":
    unittest.main()
