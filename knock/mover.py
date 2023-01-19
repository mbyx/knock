from __future__ import annotations

import random
from attrs import define

from depict import *


def random_mover(seed: int) -> Mover:
    mover = Mover()
    # Movers should be center-ish and spaced out.
    mover.position.x = seed * mover.radius + 200
    mover.mass = random.randrange(1, 8)
    # Wind of varying force either to the left or right.
    mover.add_force(Vec2[float](random.uniform(-2, 2), 0))
    # Randomize color for sex appeal.
    mover.color = Color(
        random.randrange(0, 256),
        random.randrange(0, 256),
        random.randrange(0, 256),
    )
    return mover


@define
class Mover(Circle2D):
    color: Color = color.White

    # Properties of the Mover object.
    velocity: Vec2 = Vec2[int](0, 0)
    acceleration: Vec2 = Vec2[int](0, 0)

    # Whenever mass is changed, the radius changes to reflect it visually.
    _mass: float = 1.0
    radius: float = (_mass**0.5) * 10

    friction: float = 0.02
    normal: Vec2 = Vec2[int](0, 1)

    angular_velocity: float = 0.0
    angular_acceleration: float = 0.0
    draw_: bool = True

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self._mass = mass
        self.radius = (mass**0.5) * 10

    def add_force(self, force: Vec2) -> None:
        self.acceleration += force / self.mass

    def obey_gravity(self) -> None:
        self.add_force(Vec2[float](0, 0.2 * self.mass))

    def obey_friction(self) -> None:
        self.add_force(
            -1
            * self.friction
            * self.normal.normalize().size()
            * self.velocity.normalize()
        )

    def bounce(self, engine: Engine) -> None:
        # Constrain the ball to be within the screen.
        self.position = self.position.constrain(
            Vec2[float](self.radius, self.radius),
            Vec2[float](engine.width - self.radius, engine.height - self.radius),
        )

        # if the ball collided with an edge, it should bounce and lose energy.
        if self.position.x in (engine.width - self.radius, self.radius):
            self.velocity.x *= -1

        if self.position.y in (engine.height - self.radius, self.radius):
            self.velocity.y *= -1

    def wraparound(self, engine: Engine) -> None:
        if self.position.x > engine.width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = engine.width
        if self.position.y > engine.height:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = engine.height

    def draw(self, canvas: Canvas) -> None:
        if self.draw_:
            return super().draw(canvas)

    def tick(self, delta: float, engine: Engine) -> None:
        # self.obey_gravity()
        # self.obey_friction()
        self.bounce(engine)

        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = Vec2.origin()

        self.angular_velocity += self.angular_acceleration
        self.rotation += self.angular_velocity
        self.angular_velocity *= 1 - self.friction
