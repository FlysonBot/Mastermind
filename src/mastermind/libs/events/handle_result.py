from dataclasses import field
from typing import Any, NamedTuple, Optional


class HandleResult(NamedTuple):
    """The result after handling an event."""

    handled: bool
    result: Any
    kwargs: Optional[dict[Any, Any]] = field(default_factory=dict)
