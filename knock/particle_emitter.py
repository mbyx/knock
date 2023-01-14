import random
from attrs import define
from typing import cast

from depict import *

from knock.mover import Mover


@define
class Particle(Node2D):
    position: Point = Point[int](320, 90)
    lifespan: int = 255
    decay: int = 8
    color: Color = color.White

    def dead(self) -> bool:
        return self.lifespan < 0

    def build(self) -> list[Scene]:
        return [
            Mover(
                position=self.position,
                acceleration=Vec3D(0, 0.1),
                velocity=Vec3D(random.randint(-2, 2), random.randint(0, 4)),
                color=self.color,
            )
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        self.lifespan -= self.decay
        self.position = cast(Mover, self.get_node("Mover")).position
        cast(Mover, self.get_node("Mover")).color = Color(
            self.color.r, self.color.g, self.color.b, max(0, self.lifespan)
        )


@define
class ParticleEmitter(Node2D):
    position: Point = Point[int](320, 90)
    max_particles: int = 1000
    color: Color = color.Blue

    def add_force(self, force: Vec3D) -> None:
        for particle in cast(list[Particle], self.children):
            cast(Mover, particle.get_node("Mover")).add_force(force)

    def emit(self) -> None:
        self.children.append(
            Particle(position=self.position, decay=1, color=self.color)
        )

    def tick(self, delta: float, engine: Engine) -> None:
        self.add_force(Vec2[float](0.0, 0.4))  # Gravity

        for particle in cast(list[Particle], self.children):
            if particle.dead():
                self.children.remove(particle)

        if len(self.children) < self.max_particles:
            self.emit()
