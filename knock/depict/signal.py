from __future__ import annotations
from typing import Callable, Type, TypeAlias
from attrs import astuple

from abc import ABC


class Signal(ABC):
    """A signal that can be emitted by nodes and subscribed to by others."""

    def emit(self, signals: dict[Type[Signal], list[SignalCallback]]) -> None:
        """Emit the signal such that all those subscribing are notified."""
        for callback in signals[type(self)]:
            callback(*astuple(self, recurse=False))


SignalCallback: TypeAlias = Callable[..., None]
