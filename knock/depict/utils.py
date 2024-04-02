import functools
import math
from typing import TypeVar

from attr import define

T = TypeVar("T", float, int)


def node(cls):
    """Define a node that can have signals attached to it."""
    cls.__hash__ = object.__hash__
    return define(cls, eq=False)


def map(n: T, old_min: T, old_max: T, new_min: T, new_max: T) -> float:
    """Map a value from one range to another.

    Parameters:
        `n`: The value to be mapped.
        `old_min`: The minimum value of the original range.
        `old_max`: The maximum value of the original range.
        `new_min`: The minimum value of the target range.
        `new_max`: The maximum value of the target range.

    Returns:
        `float`: The mapped value in the target range.
    """
    return (n / (old_max - old_min)) * (new_max - new_min)


def deg2rad(degrees: float) -> float:
    """Convert an angle from degrees to radians."""
    return degrees * math.pi / 180


def rad2deg(radians: float) -> float:
    """Convert an angle from radians to degrees."""
    return radians * 180 / math.pi
