from __future__ import annotations

import math, random
from typing import cast
from depict import *
from attrs import define, Factory
from knock.mover import Mover
from knock.flowfield import FlowField


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

    max_speed: float = 5.0
    max_force: float = 0.5
    separation: int = 25
    neighbour_dist: int = 40

    def build(self) -> list[Scene]:
        return [Mover("Vehicle", position=self.position, draw_=False)]

    def update_position(self, position: Point[float]) -> None:
        # Cause I don't have a brain.
        self.lines = [
            (
                (line - self.position + position)
                if not math.isclose(position.x, self.position.x)
                and not math.isclose(position.y, self.position.y)
                else line
            )
            for line in self.lines
        ]
        # Save the new position as well as set the pivot to be that position.
        self.position = position
        self.offset = position

    def seek_force(self, target: Point) -> Vec3D:
        vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
        distance: float = (target - vehicle.position).size()
        # Slow the boid down depending on distance from target.
        if distance < 100.0:
            distance = map(distance, 0, 100.0, 0, self.max_speed)
        desired: Vec3D = (target - vehicle.position).normalize() * distance
        steering: Vec3D = (desired - vehicle.velocity).constrain_size(0, self.max_force)
        return steering

    def follow(self, field: FlowField) -> None:
        vehicle: Mover = cast(Mover, self.get_node("Vehicle"))

        desired: Vec3D = field.at(self.position) * self.max_speed
        steering: Vec3D = (desired - vehicle.velocity).constrain_size(0, self.max_force)
        vehicle.add_force(steering)

    def seek(self, target: Point) -> None:
        vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
        vehicle.add_force(self.seek_force(target))

    def flee(self, target: Point) -> None:
        vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
        vehicle.add_force(-1 * self.seek_force(target))

    def separate(self, boids: list[Boid]) -> Vec3D[float]:
        resultant: Vec3D = Vec3D.origin()
        count: int = 0
        for other in boids:
            distance: float = (self.position - other.position).size()
            if self != other and distance < self.separation:
                resultant += (self.position - other.position).normalize()
                count += 1

        if count > 0:
            vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
            desired: Vec3D = (resultant / count).normalize() * self.max_speed
            steering: Vec3D = (desired - vehicle.velocity).constrain_size(
                0, self.max_force
            )
            return steering
        return Vec3D.origin()

    def align(self, boids: list[Boid]) -> Vec3D[float]:
        resultant: Vec3D = Vec3D.origin()
        count: int = 0
        for other in boids:
            other_vehicle: Mover = cast(Mover, other.get_node("Vehicle"))
            distance: float = (self.position - other.position).size()
            if self != other and distance < self.neighbour_dist:
                resultant += other_vehicle.velocity
                count += 1

        if count > 0:
            vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
            desired: Vec3D = (resultant / count).normalize() * self.max_speed
            steering: Vec3D = (desired - vehicle.velocity).constrain_size(
                0, self.max_force
            )
            return steering
        return Vec3D.origin()

    def cohesion(self, boids: list[Boid]) -> Vec3D[float]:
        resultant: Vec3D = Vec3D.origin()
        count: int = 0
        for other in boids:
            distance: float = (self.position - other.position).size()
            if self != other and distance < self.neighbour_dist:
                resultant += other.position
                count += 1

        if count > 0:
            return self.seek_force(resultant / count)
        return Vec3D.origin()

    def tick(self, delta: float, engine: Engine) -> None:
        vehicle: Mover = cast(Mover, self.get_node("Vehicle"))
        target: Point = Mouse.get_pos()

        # Limit the velocity of the boid to max_speed.
        vehicle.velocity = vehicle.velocity.constrain_size(0, self.max_speed)
        # Rotate the boid to point towards the direction it's moving.
        # velocity.angle_2d() is used instead of look_at(target)
        # so that boid doesn't instantly turn towards target.
        self.set_rotation(rad2deg(vehicle.velocity.angle_2d()))
        # self.seek(target)
        self.update_position(vehicle.position)


@define
class Flock(Scene):
    size: int = 20

    def flock(self) -> None:
        for boid in cast(list[Boid], self.children):
            vehicle: Mover = cast(Mover, boid.get_node("Vehicle"))
            vehicle.add_force(
                boid.separate(cast(list[Boid], self.children)) * random.random()
            )
            vehicle.add_force(
                boid.align(cast(list[Boid], self.children)) * random.random()
            )
            vehicle.add_force(
                boid.cohesion(cast(list[Boid], self.children)) * random.random()
            )

    def build(self) -> list[Scene]:
        return [
            Boid(
                tag=f"Boid {i}",
                color=Color.random(),
                position=(
                    pos := Point[int](
                        random.randrange(320, 340), random.randrange(180, 210)
                    )
                ),
                lines=[
                    pos + Point[int](0, -6 * 2),
                    pos + Point[int](-6, 6 * 2),
                    pos + Point[int](6, 6 * 2),
                ],
                offset=pos,
            )
            for i in range(self.size)
        ]

    def tick(self, delta: float, engine: Engine) -> None:
        self.flock()


Engine(Size(640, 360), background=color.Black).run(Flock())
