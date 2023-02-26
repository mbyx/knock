"""A swinging pendulum, with a springy string."""

import math
from typing import cast

from attrs import define
from depict import *

from knock.mover import Mover


@define
class Spring(Line2D):
    """A spring that obeys Hooke's Law."""

    length: float = 10.0
    k: float = 0.1

    def connect(self, bob: Mover) -> None:
        """Connect the spring to the bob and apply tension on it."""
        new_length: float = (bob.position - self.position).size()
        # If the spring extended, x > 0, if the spring was compressed, x < 0
        x: float = new_length - self.length
        self.end = bob.position
        # If x is compressed too much or extended too much...
        if not (-(0.50 * self.length) < x < (1.25 * self.length)):
            # Constrain x such that it isn't compressed or extended too much.
            x = min(max(x, -(0.5 * self.length)), (1.25 * self.length))
            new_constrained_length: float = self.length + x
            bob.position = self.position + (
                (bob.position - self.position).normalize() * new_constrained_length
            )
        tension = (bob.position - self.position).normalize() * -1 * self.k * x
        bob.add_force(tension)


@define
class Pendulum(Node2D):
    """A bob attached to a spring."""

    pivot: Point = Point(320, 180)
    length: float = 100.0
    # The spring starts compressed and at it's lowest height.
    position: Point = Point(pivot.x, pivot.y + length)
    radius: float = 20.0
    color: Color = Color(18, 18, 18)

    def build(self) -> list[Scene]:
        self.position: Point = Point(self.pivot.x, self.pivot.y + self.length)
        self.rotation = 90 * (math.pi / 180)
        return [
            Spring(position=self.pivot, end=self.position, length=self.length),
            Mover(
                tag="Bob",
                pivot=self.pivot,
                position=self.position,
                color=self.color,
            ),
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        bob: Mover = cast(Mover, self.get_node("Bob"))
        spring: Spring = cast(Spring, self.get_node("Spring"))

        bob.obey_gravity()
        spring.connect(bob)
