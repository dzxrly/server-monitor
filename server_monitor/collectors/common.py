from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


def safe_call(function: Callable[[], T], default: T) -> T:
    try:
        return function()
    except (AttributeError, NotImplementedError, OSError, RuntimeError, ValueError):
        return default


def nullable_number(value: Any) -> float | int | None:
    if value is None:
        return None
    if isinstance(value, int | float):
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
