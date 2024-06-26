from __future__ import annotations

"""A 3-Dimensional vector, along with various aliases."""

import math
from typing import Callable, Generic, TypeAlias, TypeVar, cast

import depict.utils as utils
from attrs import define

T = TypeVar("T", float, int)


@define
class Vec3D(Generic[T]):
    """A 3-dimensional vector with x, y, and z coordinates.

    Attributes:
        `x`: The x-coordinate of the vector.
        `y`: The y-coordinate of the vector.
        `z`: The z-coordinate of the vector (default is 0.0).

    Methods:
        `scalar`: Create a vector with all components set to a scalar value.
        `origin`: Return the vector pointing towards the origin (0, 0, 0).
        `angle_between`: Calculate the angle between two vectors in radians.
        `is_close`: Determine whether two vectors are close in value.
        `rotate`: Rotate the vector around a point by a specified angle.
        `map`: Map each component of the vector with a given function.
        `abs_diff`: Find the absolute value of the difference between two vectors.
        `as_2d`: Return a two-tuple representing the vector with the z-component stripped.
        `angle_2d`: Calculate the angle of a vector in a 2D context.
        `size`: Calculate the magnitude of the vector.
        `size_sq`: Calculate the magnitude squared of the vector.
        `normalize`: Calculate the unit vector pointing in the same direction.
        `dot`: Calculate the dot product of two vectors.
        `cross`: Calculate the cross product of two vectors.
        `constrain_size`: Constrain the magnitude of the vector between specified bounds.
        `constrain`: Constrain the components of the vector between specified bounds.

    Operators:
        `__add__`: Add the components of two vectors.
        `__sub__`: Subtract the components of two vectors.
        `__truediv__`: Divide the components of the vector by a scalar.
        `__floordiv__`: Floor divide the components of the vector by a scalar.
        `__mul__`: Multiply the components of the vector by a scalar.
        `__rmul__`: Multiply the components of the vector by a scalar.

    Note:
        For efficiency, use `size_sq` instead of `size` when possible to minimize square root operations.
    """

    x: T
    y: T
    z: T = cast(T, 0.0)

    @staticmethod
    def scalar(n: T) -> Vec3D[T]:
        """Create a vector with all components set to `n`.

        Convenience function for when you want to add or subtract a scalar
        value from all components of a vector."""
        return Vec3D(n, n, n)

    @staticmethod
    def origin() -> Vec3D[float]:
        """The vector pointing towards the origin, i.e `(0, 0, 0)`."""
        return Vec3D(0.0, 0.0, 0.0)

    def angle_between(self, other: Vec3D) -> float:
        """Calculate the angle between two vectors in radians."""
        return math.acos(self.dot(other) / ((self.size_sq() * other.size_sq()) ** 0.5))

    def is_close(self, other: Vec3D) -> bool:
        """Determine whether two vectors are close in value.

        This is essential when using floating point values, as they cannot
        be properly compared."""
        return math.isclose(self.x, other.x) and math.isclose(self.x, other.x)

    def rotate(self, degrees: float, around: Point) -> Vec3D[float]:
        """Rotate the vector around `around` by `degrees` in degrees."""
        theta: float = utils.deg2rad(degrees) % math.tau
        radius: float = (self - around).size()
        position: Vec3D[float] = cast(Vec3D[float], (self - around).normalize())
        x: float = position.dot(Vec3D(math.cos(theta), -1 * math.sin(theta)))
        y: float = position.dot(Vec3D(math.sin(theta), math.cos(theta)))
        return around + Point(x, y) * radius

    def map(self, func: Callable[[T], T]) -> Vec3D:
        """Map each of the components of a vector with some function."""
        return Vec3D(func(self.x), func(self.y), func(self.z))

    def abs_diff(self, other: Vec3D) -> Vec3D[float]:
        """Find the absolute value of the difference between two vectors."""
        return (self - other).map(abs)  # type: ignore

    def as_2d(self) -> tuple[T, T]:
        """Strip the z-component of a vector and return a two-tuple."""
        return (self.x, self.y)

    def angle_2d(self) -> float:
        """Caculate the angle of a vector in a 2D context."""
        angle: float = math.atan2(self.y, self.x)
        return angle if angle >= 0.0 else math.tau + angle

    def size(self) -> T:
        """Calculate the magnitude of a vector."""
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def size_sq(self) -> T:
        """Calculate the magnitude squared of a vector.

        This method is supposed to be used to minimize the number of square root
        operations, as they are very slow."""
        return self.x**2 + self.y**2 + self.z**2

    def normalize(self) -> Vec3D[T]:
        """Calculate the unit vector that points in the same direction as the vector."""
        # Avoid ZeroDivisionError when `Vec3D.size()` is 0.
        if (size := self.size()) != 0:
            return cast(Vec3D[T], self / size)
        else:
            return self

    def dot(self, other: Vec3D[T]) -> T:
        """Calculate the dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: Vec3D[T]) -> Vec3D[T]:
        """Calculate the cross product of two vectors."""
        return Vec3D(
            self.y * other.z - other.y * self.z,
            self.x * other.z - other.x * self.z,
            self.x * other.y - other.x * self.y,
        )

    def constrain_size(self, min_: T, max_: T) -> Vec3D[T]:
        """Constrain the magnitude of a vector to be between `min_` and `max_`."""
        return self.normalize() * min(max_, max(min_, self.size()))

    def constrain(self, min_bound: Vec3D[T], max_bound: Vec3D[T]) -> Vec3D[T]:
        """Constrain the components of a vector between bounds.

        This function takes in two vectors that specify a 2D rectangle or a 3D
        cube in which the vector must be constrained."""
        return Vec3D(
            min(max_bound.x, max(min_bound.x, self.x)),
            min(max_bound.y, max(min_bound.y, self.y)),
            min(max_bound.z, max(min_bound.z, self.z)),
        )

    def __add__(self, other: Vec3D[T]) -> Vec3D[T]:
        """Add the components of the two vectors."""
        return Vec3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: Vec3D[T]) -> Vec3D[T]:
        """Subtract the components of the two vectors."""
        return Vec3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __truediv__(self, other: T) -> Vec3D[float]:
        """Divide the components of the vector by a scalar value."""
        return Vec3D(self.x / other, self.y / other, self.z / other)

    def __floordiv__(self, other: T) -> Vec3D[int]:
        return (self / other).map(math.floor)

    def __mul__(self, other: T) -> Vec3D[T]:
        """Multiply the components of the vector by a scalar value."""
        return Vec3D(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other: T) -> Vec3D[T]:
        """Multiply the components of the vector by a scalar value."""
        return self.__mul__(other)


# A 2D Vector is just a 3D Vector with the z-component set to 0.0.
Vec2D: TypeAlias = Vec3D
# A point in 2D/3D space can be represented as a vector.
Point: TypeAlias = Vec3D


class Size(Vec3D[int]):
    """Minimal subclass of `Vec3D` with better accessors."""

    z: int = 0

    @property
    def width(self) -> int:
        return self.x

    @width.setter
    def width(self, width: int) -> None:
        self.x = width

    @property
    def height(self) -> int:
        return self.y

    @height.setter
    def height(self, height: int) -> None:
        self.y = height
