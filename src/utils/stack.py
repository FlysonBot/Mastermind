from collections import deque
from typing import Any, Optional


class Stack:
    """
    A simple stack data structure implementation using the deque from the collections module.

    Attributes:
        _stack (collections.deque): The internal deque used to store the stack elements.
    """

    def __init__(self, data: Optional[list] = None) -> None:
        """
        Initializes the Stack object with the given data (optional).

        Args:
            data (Optional[list]): The initial data to be added to the stack.
        """
        self._stack = deque(data) if data else deque()

    def push(self, item: Any) -> None:
        """
        Pushes an item onto the top of the stack.

        Args:
            item (Any): The item to be pushed onto the stack.
        """
        self._stack.append(item)

    def pop(self) -> Any:
        """
        Removes and returns the top item from the stack.

        Returns:
            Any: The top item from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("No items to pop.")
        return self._stack.pop()

    def top(self) -> Any:
        """
        Returns the top item from the stack without removing it.

        Returns:
            Any: The top item from the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if self.is_empty():
            raise IndexError("No items to top.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        return len(self._stack) == 0

    def __len__(self) -> int:
        """
        Returns the number of items in the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self._stack)

    def __getitem__(self, index: int) -> Any:
        """
        Returns the item at the specified index from the top of the stack.

        Args:
            index (int): The index of the item to retrieve, where 0 is the top of the stack.

        Returns:
            Any: The item at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= len(self._stack):
            raise IndexError("Index out of range.")
        return self._stack[-(index + 1)]

    def clear(self) -> None:
        """
        Clears all items from the stack.
        """
        self._stack.clear()

    @property
    def as_list(self) -> list:
        """
        Returns the stack as a list, with the top item first.

        Returns:
            list: The stack as a list.
        """
        return list(self._stack)

    def __iter__(self):
        """
        Returns an iterator over the stack.
        """
        return iter(self._stack)
