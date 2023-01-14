import math
from attrs import define
from typing import cast

from depict import *

from knock.mover import Mover


@define
class Spring(Line2D):
    length: float = 10.0
    k: float = 0.1

    def connect(self, bob: Mover) -> None:
        new_length: float = (bob.position - self.position).size()
        # If the spring extended, x > 0, if the spring was compressed, x < 0
        x: float = new_length - self.length
        self.end = bob.position
        # If x is compressed too much or extended too much...
        if not (-(0.50 * self.length) < x < (1.25 * self.length)):
            # Constrain x such that it isn't compressed by more than 90px and extended more than 150px
            x = min(max(x, -(0.5 * self.length)), (1.25 * self.length))
            new_constrained_length: float = self.length + x
            bob.position = self.position + (
                (bob.position - self.position).normalize() * new_constrained_length
            )
        force = (bob.position - self.position).normalize() * -1 * self.k * x
        bob.add_force(force)


@define
class Pendulum(Node2D):
    origin: Point = Point[int](320, 180)
    length: float = 100.0
    # The spring starts compressed by 20px.
    position: Point = Point[float](origin.x, origin.y + length)
    radius: float = 20.0
    color: Color = Color(18, 18, 18)

    def build(self) -> list[Scene]:
        self.position: Point = Point[int](self.origin.x, self.origin.y + self.length)
        self.rotation = 90 * (math.pi / 180)
        return [
            Spring(position=self.origin, end=self.position, length=self.length),
            Mover(
                tag="Bob",
                offset=self.offset,
                position=self.position,
                color=self.color,
            ),
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        bob: Mover = cast(Mover, self.get_node("Bob"))
        spring: Spring = cast(Spring, self.get_node("Spring"))

        bob.add_force(Vec3D(0, 0.4 * bob.mass))
        spring.connect(bob)
