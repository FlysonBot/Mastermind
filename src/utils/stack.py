from collections import deque
from typing import Any, Optional


class Stack:
    def __init__(self, data: Optional[list] = None) -> None:
        self._stack = deque(data) if data else deque()

    def push(self, item: Any) -> None:
        self._stack.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("No items to pop.")
        return self._stack.pop()

    def top(self) -> Any:
        if self.is_empty():
            raise IndexError("No items to top.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def __len__(self) -> int:
        return len(self._stack)

    def __getitem__(self, index: int) -> Any:
        if index < 0 or index >= len(self._stack):
            raise IndexError("Index out of range.")
        return self._stack[-(index + 1)]

    def clear(self) -> None:
        self._stack.clear()

    @property
    def as_list(self) -> list:
        return list(self._stack)

    def __iter__(self):
        return iter(self._stack)
