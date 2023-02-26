"""Beyblade, let it rip!"""

from attrs import define
from depict import *


@define
class SpinningLine(Line2D):
    """A line that spins..."""

    length: float = 200.0
    offset: Point = Point(320, 180)
    start: Point = Point(offset.x - (length / 2), 180)
    end: Point = Point(offset.x + (length / 2), 180)

    def tick(self, delta: float, engine: Engine) -> None:
        self.offset = Mouse.get_pos()
        # Make sure the length from the offset to end remains the same.
        self.end = self.offset + (self.end - self.offset).normalize() * (
            self.length / 2
        )
        self.end = self.end.rotate(1, around=self.offset)
        self.start = self.end.rotate(180, around=self.offset)
