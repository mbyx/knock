from depict import *
from attrs import define


@define  # Requires clear=False
class Spiral(Point2D):
    radius: float = 100.0
    offset: Point = Point[int](320, 180)
    position: Point = Point[float](offset.x + radius, offset.y)
    color: Color = Color.random()

    def tick(self, delta: float, engine: Engine) -> None:
        self.rotate(1)
        self.radius += 0.1
