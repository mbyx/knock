from depict import *
from attrs import define
from knock.liquid import Liquid
from knock.mover import random_mover


@define
class UnitCircle(Point2D):
    radius: float = 100.0
    offset: Point = Point[int](320, 180)
    position: Point = Point[float](offset.x + radius, offset.y)
    color: Color = Color.random()

    def tick(self, delta: float, engine: Engine) -> None:
        self.rotate(1)
        self.radius += 0.1


@define
class SpinningLine(Line2D):
    offset: Point = Point[int](320, 180)
    start: Point = Point[int](offset.x - 100, 180)
    end: Point = Point[int](offset.x + 100, 180)

    def tick(self, delta: float, engine: Engine) -> None:
        self.offset = Mouse.get_pos()
        # Make sure the length from the offset to end remains the same.
        self.end = self.offset + (self.end - self.offset).normalize() * 100.0
        self.end = self.end.rotate(1, around=self.offset)
        self.start = self.end.rotate(180, around=self.offset)


@define
class Boid(Polygon2D):
    # Center point of the triangle.
    position: Point = Point[int](320, 180)
    # The point about which to rotate the triangle.
    offset: Point = position
    # The vertices of a triangle.
    lines: list[Point] = [
        position + Point[int](0, -6 * 2),
        position + Point[int](-6, 6 * 2),
        position + Point[int](6, 6 * 2),
    ]
    # The angle that the triangle is initially at.
    rotation: float = deg2rad(270.0)

    def tick(self, delta: float, engine: Engine) -> None:
        self.set_rotation(rad2deg(self.angle_to(Mouse.get_pos())))


class FunStuff(Scene):
    def build(self) -> list[Scene]:
        return [Liquid(), random_mover(1)]


Engine(Size(640, 360), background=color.Black).run(FunStuff())
