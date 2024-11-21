from abc import ABC
from typing import Any

from src.validation.base.base import StateValidator


class ValidatedClass(ABC):
    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)

        while isinstance(value, StateValidator):
            value = value.value

        return value

    def __setattr__(self, name: str, value: Any) -> None:
        if hasattr(self, name):
            attr = super().__getattribute__(name)

            if isinstance(attr, StateValidator):
                attr.value = value  # invoke setter method to validate modification
                return

        super().__setattr__(name, value)
