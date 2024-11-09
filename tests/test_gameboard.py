import unittest
from ..gameboard import *


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_push_and_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_top(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.top(), 2)
        self.stack.pop()
        self.assertEqual(self.stack.top(), 1)
        self.stack.pop()
        with self.assertRaises(IndexError):
            self.stack.top()

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.stack.push(1)
        self.assertFalse(self.stack.is_empty())
        self.stack.pop()
        self.assertTrue(self.stack.is_empty())

    def test_length(self):
        self.assertEqual(len(self.stack), 0)
        self.stack.push(1)
        self.assertEqual(len(self.stack), 1)
        self.stack.push(2)
        self.assertEqual(len(self.stack), 2)
        self.stack.pop()
        self.assertEqual(len(self.stack), 1)
        self.stack.pop()
        self.assertEqual(len(self.stack), 0)

    def test_get_item(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack[0], 2)
        self.assertEqual(self.stack[1], 1)
        with self.assertRaises(IndexError):
            self.stack[2]

    def test_clear_stack(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.clear_stack()
        self.assertTrue(self.stack.is_empty())

    def test_iter(self):
        self.stack.push(1)
        self.stack.push(2)
        items = list(self.stack)
        self.assertEqual(items, [1, 2])  # Note: Order is from bottom to top.


if __name__ == "__main__":
    unittest.main()
