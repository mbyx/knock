from __future__ import annotations

"""An object that... moves?"""

import random

from attrs import define
from depict import *


def random_mover(seed: int) -> Mover:
    """Create a Mover with randomized properties."""
    mover = Mover()
    # Movers should be center-ish and spaced out.
    mover.position.x = seed * mover.radius + 200
    mover.mass = random.randrange(1, 8)
    # Wind of varying force either to the left or right.
    # Note: This force is only added for one timestep.
    mover.add_force(Vec2D(random.uniform(-2, 2), 0))
    # Randomize color for sex appeal.
    mover.color = Color.random()
    return mover


@define
class Mover(Circle2D):
    """An object that can move with a velocity and acceleration."""

    color: Color = White

    velocity: Vec2D = Vec2D(0, 0)
    acceleration: Vec2D = Vec2D(0, 0)

    # Whenever mass is changed, the radius changes to reflect it visually.
    _mass: float = 1.0
    radius: float = (_mass**0.5) * 10

    friction: float = 0.02
    normal: Vec2D = Vec2D(0, 1)
    g: float = 0.2
    restitution: float = 0.98

    angular_velocity: float = 0.0
    angular_acceleration: float = 0.0

    # TODO: Make this a generic part of a Scene.
    # Whether to draw the shape or not.
    draw_: bool = True

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, mass: float) -> None:
        self._mass = mass
        self.radius = (mass**0.5) * 10

    def add_force(self, force: Vec2D) -> None:
        """Add a force to the Mover, using `F = ma`."""
        self.acceleration += force / self.mass

    def obey_gravity(self) -> None:
        """Apply a crude gravity on the Mover according to its mass."""
        weight: Vec2D = Vec2D(0, self.g * self.mass)
        self.add_force(weight)

    def obey_friction(self) -> None:
        """Apply a crude frictional force on the Mover."""
        friction: Vec2D = (
            -1 * self.friction * self.normal.size() * self.velocity.normalize()
        )
        self.add_force(friction)

    def bounce(self, engine: Engine) -> None:
        """Allow the ball to bounce around the screen on hitting an edge."""
        # Constrain the ball to be within the screen.
        self.position = self.position.constrain(
            Vec2D(self.radius, self.radius),
            Vec2D(engine.width - self.radius, engine.height - self.radius),
        )

        # if the ball collided with an edge, it should bounce and lose energy.
        if self.position.x in (engine.width - self.radius, self.radius):
            self.velocity.x *= -self.restitution

        if self.position.y in (engine.height - self.radius, self.radius):
            self.velocity.y *= -self.restitution

    def wraparound(self, engine: Engine) -> None:
        """When the ball reaches the screen edges, it should wrap around."""
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
        # Newton's algorithm
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = Vec2D.origin()

        self.angular_velocity += self.angular_acceleration
        self.rotation += self.angular_velocity
        self.angular_velocity *= 1 - self.friction
