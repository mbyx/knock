"""It's a bird, it's a plane, it's a boid!"""

from __future__ import annotations

from typing import cast

from attrs import define
from depict import *
from flowfield import FlowField
from mover import Mover


@define
class Boid(Polygon2D):
    """A 2D triangle representing a bird with numerous steering behaviours."""

    # Center point of the triangle.
    position: Point = Point(320, 180)

    # The angle that the triangle is initially at.
    rotation_: float = utils.deg2rad(270.0)
    last_position: Vec3D = Vec3D.origin()

    # The rest of the properties are defined in ready() as they depend on position.

    # Configure the flocking simulation using these variables.
    max_speed: float = 8.0
    max_force: float = 1.0
    arrival_dist: float = 100.0

    def ready(self, engine: Engine) -> None:
        # The point about which to rotate the triangle.
        self.pivot: Point = self.position
        # The vertices of a triangle.
        self.lines: list[Point] = [
            self.position + Point(0, -6 * 2),
            self.position + Point(-6, 6 * 2),
            self.position + Point(6, 6 * 2),
        ]
        self.last_position = self.position

    def build(self) -> list[Scene]:
        # We require a moveable object, so attach a Mover that is set
        # to be invisible.
        return [Mover("Vehicle", position=self.position, draw_=False)]

    def moved(self, last_position: Point, position: Point) -> Point:
        """Called whenever the Boid moves."""
        # If the position hasn't changed by much, do not update `lines`.
        # Reset each line to origin then add the new position.
        self.lines = [((line - last_position + position)) for line in self.lines]

        # Save the new position and set the pivot to be at that position.
        self.position = position
        self.pivot = position

        return position

    def seek_force(self, target: Point, mover: Mover) -> Vec3D:
        """Calculate a force that points towards a target."""
        distance: float = (target - mover.position).size_sq()
        # Slow down the boid if it is close to the target.
        if distance < self.arrival_dist**2:
            distance = utils.map(distance, 0, self.arrival_dist, 0, self.max_speed)

        desired: Vec3D = (target - mover.position).normalize() * distance
        steering: Vec3D = (desired - mover.velocity).constrain_size(0, self.max_force)
        return steering

    def follow(self, field: FlowField, mover: Mover) -> None:
        """Follow the flow of vectors in the FlowField."""
        desired: Vec3D = field.at(self.position) * self.max_speed
        steering: Vec3D = (desired - mover.velocity).constrain_size(0, self.max_force)
        mover.add_force(steering)

    def seek(self, target: Point, mover: Mover) -> None:
        """Seek an object, either static or dynamic."""
        mover.add_force(self.seek_force(target, mover))

    def flee(self, target: Point, mover: Mover) -> None:
        """Escape from an object, whether it is moving or not."""
        mover.add_force(-1 * self.seek_force(target, mover))

    def tick(self, delta: float, engine: Engine) -> None:
        mover: Mover = cast(Mover, self.get_node("Vehicle"))

        self.last_position: Point = self.moved(self.last_position, mover.position)
        # Limit the velocity of the boid to max_speed.
        mover.velocity = mover.velocity.constrain_size(0, self.max_speed)
        # Rotate the boid to point towards the direction it's moving.
        # velocity.angle_2d() is used instead of look_at(target)
        # so that boid doesn't instantly turn towards target.
        self.rotation_ = utils.rad2deg(mover.velocity.angle_2d())
