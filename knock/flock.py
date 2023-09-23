from __future__ import annotations

"""A flocking simulation."""

import random
from typing import cast

from attrs import define
from boid import Boid
from depict import *
from mover import Mover

# TODO: Tweak the flocking parameters to make a better simulation.
# TODO: Ideally allow hot reloading these parameters via sliders.
# TODO: Optimize to use a dynamic quadtree.


@define
class Flock(Scene):
    """A flocking simulation."""

    # Size of the flock; very large values will run slowly.
    size: int = 45
    separation: int = 60
    neighbour_dist: int = 90
    weights: list[float] = [1.25, 1.5, 1.75]

    def flock_forces(self, boids: list[Boid], boid: Boid) -> tuple[Vec3D, Vec3D, Vec3D]:
        """Calculate the separation, alignment, and cohesion forces all at once."""
        # Store each force in a tuple, representing the total force and the
        # number of boids this force interacts with.
        separation_force = alignment_force = cohesion_force = Vec3D.origin()

        separate: tuple[Vec3D, int] = (Vec3D.origin(), 0)
        align: tuple[Vec3D, int] = (Vec3D.origin(), 0)
        cohesion: tuple[Vec3D, int] = (Vec3D.origin(), 0)

        mover: Mover = cast(Mover, boid.get_node("Vehicle"))

        # TODO: Refactor.
        for other in boids:
            direction: Vec3D = (boid.position - other.position).normalize()
            distance: float = direction.size_sq()
            if boid == other:
                continue

            other_mover: Mover = cast(Mover, other.get_node("Vehicle"))
            if distance < self.separation**2:
                separate = (separate[0] + direction, separate[1] + 1)
            if distance < self.neighbour_dist**2:
                align = (align[0] + other_mover.velocity, align[1] + 1)
                cohesion = (cohesion[0] + other.position, cohesion[1] + 1)

        # If any boids were interacted with.
        if separate[1] > 0:
            desired: Vec3D = (separate[0] / separate[1]).normalize() * boid.max_speed
            separation_force: Vec3D = (desired - mover.velocity).constrain_size(
                0, boid.max_force
            )

        if align[1] > 0:
            desired: Vec3D = (align[0] / align[1]).normalize() * boid.max_speed
            alignment_force: Vec3D = (desired - mover.velocity).constrain_size(
                0, boid.max_force
            )
        if cohesion[1] > 0:
            cohesion_force: Vec3D = boid.seek_force(cohesion[0] / cohesion[1], mover)

        return separation_force, alignment_force, cohesion_force

    def flock(self) -> None:
        """Apply the forces necessary for the flock to... flock."""
        for boid in cast(list[Boid], self.children):
            mover: Mover = cast(Mover, boid.get_node("Vehicle"))
            separation, alignment, cohesion = self.flock_forces(
                cast(list[Boid], self.children), boid
            )
            mover.add_force(separation * self.weights[0])
            mover.add_force(alignment * self.weights[1])
            mover.add_force(cohesion * self.weights[2])

    def build(self) -> list[Scene]:
        return [
            Boid(
                tag=f"Boid {i}",
                color=Color.random(),
                position=Point(random.randrange(320, 340), random.randrange(180, 210)),
            )
            for i in range(self.size)
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        self.flock()
