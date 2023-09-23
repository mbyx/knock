"""A mesmerising spiral."""

from attrs import define
from depict import *


@define
class Spiral(Point2D):
    """A mesmerising spiral.

    Requires clear=False to be set."""

    radius: float = 1.0
    pivot: Point = Point(320, 180)
    position: Point = Point(pivot.x + radius, pivot.y)
    color: Color = Color.random()

    def tick(self, delta: float, engine: Engine) -> None:
        direction: Vec3D = (self.position - self.pivot).normalize()
        old_radius = direction * self.radius
        self.radius += 0.1
        self.position = self.position + (direction * self.radius - old_radius)
        self.rotate(1)
