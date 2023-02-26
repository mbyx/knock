"""A mesmerising spiral."""

from attrs import define
from depict import *


@define
class Spiral(Point2D):
    """A mesmerising spiral.

    Requires clear=False to be set."""

    radius: float = 100.0
    offset: Point = Point(320, 180)
    position: Point = Point(offset.x + radius, offset.y)
    color: Color = Color.random()

    def tick(self, delta: float, engine: Engine) -> None:
        self.rotate(1)
        self.radius += 0.1
