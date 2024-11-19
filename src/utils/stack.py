from collections import deque
from typing import Any, Optional


class Stack:
    """An implementation of a stack data structure using deque."""

    def __init__(self, data: Optional[list] = None) -> None:
        """Initializes the stack."""
        self._stack = deque(data) if data else deque()

    def push(self, item: Any) -> None:
        """Adds an item to the top of the stack."""
        self._stack.append(item)

    def pop(self) -> Any:
        """Removes and returns the top item from the stack."""
        if self.is_empty():
            raise IndexError("No items to pop.")
        return self._stack.pop()

    def top(self) -> Any:
        """Returns the top item from the stack without removing it."""
        if self.is_empty():
            raise IndexError("No items to top.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        """Returns True if the stack is empty, False otherwise."""
        return len(self._stack) == 0

    def __len__(self) -> int:
        """Returns the number of items in the stack."""
        return len(self._stack)

    def __getitem__(self, index: int) -> Any:
        """Returns the item at the given index counted from the top."""
        if index < 0 or index >= len(self._stack):
            raise IndexError("Index out of range.")
        return self._stack[-(index + 1)]

    def clear(self) -> None:
        """Clears the stack."""
        self._stack.clear()

    @property
    def as_list(self) -> list:
        """Returns the stack as a list. DO NOT EDIT THIS LIST."""
        return list(self._stack)

    def __iter__(self):
        """Return an iterator for the stack."""
        return iter(self._stack)
