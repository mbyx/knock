"""A particle system that can be affected by physics."""

import random
from typing import cast

from attrs import define
from depict import *
from simulations.mover import Mover


@define
class Particle(Node2D):
    """A Mover that decays over time."""

    position: Point = Point(320, 90)
    lifespan: int = 255  # Lifespan goes from 0-255, for the alpha channel.
    decay_rate: int = 8
    color: Color = White

    def dead(self) -> bool:
        """Determines whether the particle is dead."""
        return self.lifespan < 0

    def build(self) -> list[Scene]:
        return [
            Mover(
                tag="Particle",
                position=self.position,
                acceleration=Vec3D(0, 0.1),
                velocity=Vec3D(random.randint(-2, 2), random.randint(0, 4)),
                color=self.color,
            )
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        self.lifespan -= self.decay_rate

        particle: Mover = cast(Mover, self.get_node("Particle"))
        self.position = particle.position

        particle.color.a = max(0, self.lifespan)


@define
class ParticleEmitter(Node2D):
    """A point source of particles being emitted."""

    position: Point = Point(320, 90)
    max_particles: int = 1000
    color: Color = Blue

    def add_force(self, force: Vec3D) -> None:
        """Add a force to every single particle that exists."""
        for particle in cast(list[Particle], self.children):
            cast(Mover, particle.get_node("Mover")).add_force(force)

    def emit(self) -> None:
        """Emit a new particle."""
        self.children.append(
            Particle(position=self.position, decay_rate=8, color=self.color)
        )

    def tick(self, delta: float, engine: Engine) -> None:
        for particle in cast(list[Particle], self.children):
            cast(Mover, particle.get_node("Particle")).obey_gravity()
            if particle.dead():
                self.children.remove(particle)

        if len(self.children) < self.max_particles:
            self.emit()
