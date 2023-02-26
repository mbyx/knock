"""Fractal Tree-ish."""

from attrs import define
from depict import *

# TODO: Refactor.


@define
class FractalTree(Node2D):
    """A tree made up of fractal patterns."""

    position: Point = Point(320, 360)
    length: float = 60.0

    def line(self, start: Point, end: Point, size: Size) -> None:
        """Create a fractal line from start to end that is affected by the mouse."""
        length: float = (end - start).size()
        if length < 2.0:
            return

        theta: float = utils.map(Mouse.get_pos().x, 0, size.width, 0, size.height)
        self.children.append(Line2D(start=start, end=end))
        self.line(end, Point(end.x, end.y - length * 2 / 3).rotate(theta, end), size)
        self.line(end, Point(end.x, end.y - length * 2 / 3).rotate(-theta, end), size)

    def tick(self, delta: float, engine: Engine) -> None:
        end: Point = Point(self.position.x, self.position.y - self.length)
        self.line(self.position, end, engine.size)

    def draw(self, canvas: Canvas) -> None:
        self.children = []
        return super().draw(canvas)
