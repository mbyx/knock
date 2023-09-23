from __future__ import annotations

from typing import TYPE_CHECKING

from attrs import Factory, define

import depict.color as color
import depict.utils as utils
from depict.color import Color
from depict.nodes import Node2D
from depict.vec3d import Point, Size

if TYPE_CHECKING:
    from depict.canvas import Canvas


@define
class Circle2D(Node2D):
    """A 2D Circle that can be drawn onto a canvas."""

    radius: float = 10.0
    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.circle(self.position, self.radius, self.color)


@define
class Point2D(Node2D):
    """A 2D point that is drawable on a canvas."""

    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.point(self.position, self.color)


@define
class Line2D(Node2D):
    """A 2D line that is drawable on a canvas."""

    start: Point = Factory(Point.origin)
    end: Point = Factory(Point.origin)
    position: Point = end
    color: Color = color.White
    width: int = 1

    def draw(self, canvas: Canvas) -> None:
        canvas.line(self.start, self.end, self.color, self.width)


@define
class Rect2D(Node2D):
    """A 2D rectangle that is drawable on a canvas."""

    size: Size = Size(20, 20)
    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.rect(self.position, self.size, self.color)


@define
class Polygon2D(Node2D):
    """A 2D polygon that can be drawn on a canvas."""

    lines: list[Point] = Factory(list)
    color: Color = color.White

    @Node2D.rotation.setter
    def rotation(self, degrees: float) -> None:
        self.lines = [
            line.rotate(degrees - utils.rad2deg(self.rotation), around=self.pivot)
            for line in self.lines
        ]
        self._rotation = utils.deg2rad(degrees)

    def rotate(self, degrees: float) -> None:
        self.lines = [line.rotate(degrees, around=self.pivot) for line in self.lines]
        self._rotation += utils.deg2rad(degrees)

    def draw(self, canvas: Canvas) -> None:
        canvas.polygon(self.lines, self.color)
