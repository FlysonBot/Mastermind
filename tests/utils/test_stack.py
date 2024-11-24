import unittest

from src.utils.stack import Stack


class TestStack(unittest.TestCase):
    """Test suite for the Stack class"""

    def test_init(self):
        """Test that Stack can be initialized with or without data"""
        stack1 = Stack()
        self.assertEqual(len(stack1), 0)

        stack2 = Stack([1, 2, 3])
        self.assertEqual(len(stack2), 3)

    def test_push(self):
        """Test that items can be pushed onto the stack"""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack.top(), 3)

    def test_pop(self):
        """Test that items can be popped from the stack"""
        stack = Stack([1, 2, 3])
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(len(stack), 2)
        self.assertEqual(stack.top(), 2)

    def test_pop_empty_stack(self):
        """Test that popping from an empty stack raises an IndexError"""
        stack = Stack()
        with self.assertRaises(IndexError) as context:
            stack.pop()
        self.assertEqual(str(context.exception), "No items to pop.")

    def test_top(self):
        """Test that the top item can be retrieved from the stack"""
        stack = Stack([1, 2, 3])
        self.assertEqual(stack.top(), 3)
        self.assertEqual(len(stack), 3)

    def test_top_empty_stack(self):
        """Test that retrieving the top item from an empty stack raises an IndexError"""
        stack = Stack()
        with self.assertRaises(IndexError) as context:
            stack.top()
        self.assertEqual(str(context.exception), "No items to top.")

    def test_is_empty(self):
        """Test that the is_empty method works correctly"""
        stack = Stack()
        self.assertTrue(stack.is_empty())

        stack.push(1)
        self.assertFalse(stack.is_empty())

    def test_len(self):
        """Test that the __len__ method works correctly"""
        stack = Stack([1, 2, 3])
        self.assertEqual(len(stack), 3)

    def test_getitem(self):
        """Test that the __getitem__ method works correctly"""
        stack = Stack([1, 2, 3, 4, 5])
        self.assertEqual(stack[0], 5)
        self.assertEqual(stack[2], 3)
        with self.assertRaises(IndexError) as context:
            _ = stack[5]
        self.assertEqual(str(context.exception), "Index out of range.")

    def test_clear(self):
        """Test that the clear method works correctly"""
        stack = Stack([1, 2, 3])
        self.assertEqual(len(stack), 3)
        stack.clear()
        self.assertEqual(len(stack), 0)

    def test_as_list(self):
        """Test that the as_list property works correctly"""
        stack = Stack([1, 2, 3])
        self.assertEqual(stack.as_list, [1, 2, 3])

    def test_iteration(self):
        """Test that the stack can be iterated over"""
        stack = Stack([1, 2, 3])
        self.assertEqual(list(stack), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
