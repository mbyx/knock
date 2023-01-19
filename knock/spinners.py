from attrs import define
from depict import *


@define
class SpinningLine(Line2D):
    offset: Point = Point[int](320, 180)
    start: Point = Point[int](offset.x - 100, 180)
    end: Point = Point[int](offset.x + 100, 180)

    def tick(self, delta: float, engine: Engine) -> None:
        self.offset = Mouse.get_pos()
        # Make sure the length from the offset to end remains the same.
        self.end = self.offset + (self.end - self.offset).normalize() * 100.0
        self.end = self.end.rotate(1, around=self.offset)
        self.start = self.end.rotate(180, around=self.offset)
