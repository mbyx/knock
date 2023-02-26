"""The Cantor Set, aka another Fractal!"""

from attrs import define
from depict import *


@define
class CantorSet(Node2D):
    """Visualisation of the Cantor Set."""

    length: float = 600.0
    position: Point = Point(20, 0)
    color: Color = White

    def cantor_line(self, canvas: Canvas, pos: Point, length: float) -> None:
        """Create a line that recursively break down in one thirds."""
        if length <= 1.0:  # Base case; we don't need less than 1px of detail.
            return
        position: Point = Point(pos.x, pos.y + 20)

        end: Point = Point(position.x + length, position.y)
        canvas.line(position, end, self.color, width=5)

        self.cantor_line(canvas, position, length / 3)

        start: Point = Point(position.x + length * 2 / 3, position.y)
        self.cantor_line(canvas, start, length / 3)

    def draw(self, canvas: Canvas) -> None:
        self.cantor_line(canvas, self.position, self.length)
