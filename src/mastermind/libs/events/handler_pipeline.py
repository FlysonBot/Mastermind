import inspect
from abc import abstractmethod
from typing import Any, Callable

from mastermind.libs.events.handle_result import HandleResult

InstanceMethod = Callable[["HandlerPipeline"], Any]


class HandlerPipeline:
    def __init_subclass__(cls) -> None:
        """Add all methods to the handlers list in the order they were defined.

        This is done to ensure that the handlers are called in the order they were defined.
        """
        super().__init_subclass__()

        cls.handlers: list[InstanceMethod] = []
        for base in cls.__bases__:
            for attr_name, attr_value in inspect.getmembers(base):
                if inspect.isfunction(attr_value) and not attr_name.startswith("_"):
                    cls.handlers.append(attr_value)

    @classmethod
    def _add_handler_after(
        cls,
        handler: InstanceMethod,
        after: InstanceMethod,
    ) -> None:
        """Add a handler to the class after another handler.

        Args:
            handler (callable): The handler function to add (should take self as the first argument).
            after (callable): The handler function in the class that goes before the new handler.

        Raises:
            ValueError: If the *after* handler is not found in the class.
        """
        if after not in cls.handlers:
            raise ValueError(f"Handler {after} not found in {cls.__name__}")

        setattr(cls, handler.__name__, handler)
        cls.handlers.insert(cls.handlers.index(after) + 1, handler)

    @abstractmethod
    def __new__(cls, **kwargs: dict[Any, Any]) -> HandleResult:
        """Handle the event."""
