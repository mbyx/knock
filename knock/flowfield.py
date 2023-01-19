from __future__ import annotations

from depict import *
from attrs import define, Factory
from perlin_noise import PerlinNoise
import random, math

noise: PerlinNoise = PerlinNoise()


@define
class FlowField(Scene):
    """A grid of vectors representing a fluid flow."""

    resolution: int = 10
    rows: int = 640 // resolution
    cols: int = 360 // resolution
    field: list[list[Vec3D]] = Factory(list)

    def draw(self, canvas: Canvas) -> None:
        for i, row in enumerate(self.field):
            if i % 2 == 0:
                continue
            for j, velocity in enumerate(row):
                if i % 2 == 0:
                    continue
                start = Vec3D(
                    i * self.resolution + self.resolution // 2,
                    j * self.resolution + self.resolution // 2,
                )
                canvas.line(
                    start,
                    start + (start + velocity).normalize() * 5,
                    color.White,
                    width=1,
                )
                canvas.circle(
                    start + (start + velocity).normalize() * 5, 2.0, color.Red
                )

    def random(self) -> FlowField:
        """Create a random flow field with Perlin Noise."""
        self.field = [([Vec3D.origin()] * self.cols) for _ in range(self.rows)]
        dx = dy = random.randrange(10, 100)
        for row in range(self.rows):
            for col in range(self.cols):
                theta: float = map(noise([dx, dy]), 0, 1, 0, math.tau)
                self.field[row][col] = Vec3D(math.cos(theta), math.sin(theta))
                dy += 0.01
            dx += 0.01
        return self

    def at(self, pos: Point[int]) -> Vec3D:
        """Lookup the velocity vector stored at a certain position."""
        size = (pos // self.resolution).constrain(
            Vec3D.origin().map(int), Vec3D(self.rows - 1, self.cols - 1)
        )
        return self.field[size.x][size.y]
