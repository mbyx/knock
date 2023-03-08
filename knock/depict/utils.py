import math
from typing import TypeVar

T = TypeVar("T", float, int)


def map(n: T, old_min: T, old_max: T, new_min: T, new_max: T) -> float:
    """Map a value from one range to another."""
    return (n / (old_max - old_min)) * (new_max - new_min)


def deg2rad(degrees: float) -> float:
    """Convert an angle from degrees to radians."""
    return degrees * math.pi / 180


def rad2deg(radians: float) -> float:
    """Convert an angle from radians to degrees."""
    return radians * 180 / math.pi
