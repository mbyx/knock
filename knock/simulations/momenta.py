from __future__ import annotations

import math
import random
from typing import Optional, cast

from attrs import define
from depict import *
from simulations.mover import Mover


@define
class Ball(Mover):
    """A round, colorful ball."""

    @staticmethod
    def random(bounds: Size) -> Ball:
        """Randomly generate a ball that is within some bounds."""
        ball: Ball = Ball(color=Color.random())
        ball.mass = random.uniform(0.5, 5)
        radius: int = int(ball.radius)
        x: int = random.randint(radius, bounds.width - radius)
        y: int = random.randint(radius, bounds.height - radius)
        ball.position = Point(x, y)
        return ball

    def collides_with(self, other: Ball) -> bool:
        """Determine whether the two balls collide."""
        # If the sum of their radii is greater than the distance between
        # their centers, then the ball is not colliding.
        return (self.position - other.position).size() <= (other.radius + self.radius)

    def tick(self, delta: float, engine: Engine) -> None:
        self.obey_friction()
        self.bounce(engine)

        return super().tick(delta, engine)


@define
class Trigger(Scene):
    """Handles applying a velocity to the balls when the mouse is pressed."""

    engaged: bool = False
    strain: float = 0.10
    ball: Ball | None = None

    def inside_ball(self, ball: Ball) -> bool:
        """Determine whether the trigger is active for some ball."""
        # Mouse is inside circle if the distance between it and the center
        # is less than the radius...
        distance: float = (Mouse.get_pos() - ball.position).size()
        return distance <= ball.radius

    def activate(self, ball: Ball) -> None:
        """Given a ball, activate the trigger, if it is allowed."""
        distance: float = (Mouse.get_pos() - ball.position).size()

        # If we are inside a ball and the trigger isn't already active,
        # if the left mouse is pressed, draw a trigger line.
        # if the right mouse is pressed, drag the ball without any velocity.
        if self.inside_ball(ball) and not self.engaged:
            if Mouse.is_pressed(MouseButton.Left):
                self.children.append(
                    Line2D(start=ball.position, end=Mouse.get_pos(), color=Blue)
                )
                self.ball = ball
                self.engaged = True

        trigger: Line2D | None = cast(Optional[Line2D], self.get_node("Line2D"))
        if trigger is not None:
            if self.ball is not None:
                trigger.start = self.ball.position
            trigger.end = Mouse.get_pos()

        if (
            not Mouse.is_pressed(MouseButton.Left)
            and trigger is not None
            and self.ball is not None
        ):
            self.children.remove(trigger)
            self.engaged = False
            # Apply a force on the ball in the trigger direction.
            theta: float = math.tau + (Mouse.get_pos() - self.ball.position).angle_2d()
            x: float = (distance * self.strain) * math.cos(theta)
            y: float = (distance * self.strain) * math.sin(theta)
            self.ball.add_force(Vec2D(x, y))
            self.ball = None


@define
class Momenta(Scene):
    size: int = 50
    bounds: Size = Size(640, 360)

    def build(self) -> list[Scene]:
        children: list[Scene] = [Ball.random(self.bounds) for _ in range(self.size)]
        children.append(Trigger())
        return children

    def tick(self, delta: float, engine: Engine) -> None:
        for ball in cast(list[Ball], self.children[:-1]):
            trigger: Trigger = cast(Trigger, self.get_node("Trigger"))
            trigger.activate(ball)

            for other in cast(list[Ball], self.children[:-1]):
                if ball == other:
                    continue
                if ball.collides_with(other):
                    distance: float = (ball.position - other.position).size()
                    gamma: float = 0.5 * (distance - (ball.radius + other.radius))
                    overlap: Point = gamma * (ball.position - other.position) / distance
                    ball.position -= overlap
                    other.position += overlap

                    normal: Point = (other.position - ball.position).normalize()
                    tangent: Point = Point(-normal.y, normal.x)
                    ball_tan_dot = tangent.dot(ball.velocity)
                    other_tan_dot = tangent.dot(other.velocity)
                    ball_norm_dot = normal.dot(ball.velocity)
                    other_norm_dot = normal.dot(other.velocity)
                    m1 = (
                        ball_norm_dot * (ball.mass - other.mass)
                        + 2 * other.mass * other_norm_dot
                    ) / (ball.mass + other.mass)
                    m2 = (
                        other_norm_dot * (other.mass - ball.mass)
                        + 2 * ball.mass * ball_norm_dot
                    ) / (ball.mass + other.mass)

                    ball.velocity = normal * m1 + tangent * ball_tan_dot
                    other.velocity = normal * m2 + tangent * other_tan_dot
