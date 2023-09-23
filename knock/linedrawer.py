from typing import cast

from attrs import define
from depict import *


@define
class CursorLine(Point2D):
    position: Point = Point(0, 0)
    color: Color = Blue
    line_started: bool = False
    start_pos: Point = Point(0, 0)

    def tick(self, delta: float, engine: Engine) -> None:
        self.position = Mouse.get_pos()
        if Mouse.is_pressed(MouseButton.Left) and not self.line_started:
            self.start_pos: Point = self.position
            self.line_started = True
            line = Line2D(
                start=self.start_pos, end=Mouse.get_pos(), color=Color.random()
            )
            self.children.append(line)
        elif Mouse.is_pressed(MouseButton.Left) and self.line_started:
            cast(Line2D, self.children[-1]).end = Mouse.get_pos()
        else:
            self.line_started = False

        if Mouse.is_pressed(MouseButton.Right):
            try:
                del self.children[-1]
            except IndexError:
                pass


Engine(Size(640, 360), record=True).run(CursorLine())
