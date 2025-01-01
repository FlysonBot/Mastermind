from abc import abstractmethod
from typing import Any

from mastermind.libs.events.handle_result import HandleResult
from mastermind.libs.events.handler_pipeline import HandlerPipeline


class BoolHandlerPipeline(HandlerPipeline):
    """Collection of a series of bool handlers that will be called in order to handle an event. Each handler return a bool indicating whether the event was handled successfully.

    If a handler returns False, the next handler will not be called and a HandleResult with handled=False will be returned. Otherwise, the next handler will be called, and a HandleResult with handled=True will be returned if all handlers return True.
    """

    def __new__(cls, **kwargs: dict[Any, Any]) -> HandleResult:  # type: ignore
        instance = object.__new__(cls)
        instance.__dict__.update(kwargs)

        return next(
            (
                HandleResult(handled=False, result=instance._package_result())
                for handler in cls.handlers
                if not handler(instance)  # handler expected to return a bool
            ),
            HandleResult(handled=True, result=instance._package_result()),
        )

    @abstractmethod
    def _package_result(self) -> Any:
        """Package the result of the event handling into a single object."""
