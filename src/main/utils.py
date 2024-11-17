from collections import deque
from typing import Any, Optional, Tuple
import pandas as pd


def get_feedback(guess: tuple, secret: tuple, number_of_colors: int) -> list:
    """Returns the feedback for a given guess."""
    # Optimized abstract algorithm (assuming correct input)
    list1 = [0] * (number_of_colors + 1)  # black pegs + color count of guess
    list2 = [0] * (number_of_colors + 1)  # white pegs + color count of secret

    # Count colors in guess and secret code
    for dot1, dot2 in zip(guess, secret):
        if dot1 == dot2:  # if exact match found
            list1[0] += 1  # black pegs count += 1
        else:  # otherwise increment the color count to find potential white pegs
            list1[dot1] += 1  # count of color in guess += 1
            list2[dot2] += 1  # count of color in secret += 1

    # Iterate through color count (skip pegs count) to count white pegs
    for count1, count2 in zip(list1[1:], list2[1:]):
        list2[0] += min(count1, count2)  # list2[0] is white pegs count

    return list1[0], list2[0]  # return black and white pegs count


def render_dataframe(df: pd.DataFrame):
    # Calculate maximum width for each column
    col_widths = [
        max(len(str(df[col].name)), df[col].astype(str).map(len).max())
        for col in df.columns
    ]

    # Print the header with dynamic widths
    header = df.columns
    print(" ".join(f"{header[i]:<{col_widths[i]}}" for i in range(len(header))))

    # Print each row with dynamic widths
    for index, row in df.iterrows():
        print(
            " ".join(
                f"{str(row[col]):<{col_widths[i]}}" for i, col in enumerate(df.columns)
            )
        )


class FStringTemplate:
    """A class to represent a formatted string template."""

    def __init__(self, template: str) -> None:
        """Initialize with a template string."""
        self.template = template

    def eval(self, **kwargs):
        """Evaluate the template with the given keyword arguments."""
        return self.template.format(**kwargs)


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
