from typing import cast

from attrs import define
from depict import *

# TODO: Instead of drawing a single side of the snowflake, draw the whole snowflake.


@define
class KochSnowflake(Scene):
    """A visualization of one side of the Koch Snowflake."""

    def build(self) -> list[Scene]:
        start: Point = Point(160, 90)
        end: Point = Point(480, 90)
        return [
            Line2D(position=start, end=end),
            Line2D(position=start, end=end.rotate(60.0, start)),
            Line2D(position=start.rotate(300.0, end), end=end),
        ]

    def generate(self, n: int) -> None:
        """Generate the Koch fractal pattern up to a certain depth."""
        for _ in range(n):
            lines: list[Line2D] = []
            for line in cast(list[Line2D], self.children):
                a: Point = line.position
                b: Point = ((line.end - line.position) / 3) + line.position
                d: Point = ((line.end - line.position) * 2 / 3) + line.position
                c: Point = d.rotate(-60.0, b)
                e: Point = line.end

                lines.append(Line2D(position=a, end=b))
                lines.append(Line2D(position=b, end=c))
                lines.append(Line2D(position=c, end=d))
                lines.append(Line2D(position=d, end=e))
            self.children = cast(list[Scene], lines)

    def ready(self, engine: Engine) -> None:
        self.generate(7)
