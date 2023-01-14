from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import pygame
import pygame_gui as pg
from attrs import Factory, define

import knock.depict.color as color
from knock.depict.color import Color
from knock.depict.engine import MANAGER, Engine
from knock.depict.misc import Font
from knock.depict.scene import Scene
from knock.depict.signal import Signal
from knock.depict.vec3d import Point, Size, Vec3D, deg2rad, rad2deg

if TYPE_CHECKING:
    from depict.canvas import Canvas


@define
class Node2D(Scene):
    """A node with a position and rotation."""

    position: Vec3D = Factory(Vec3D.origin)
    offset: Vec3D = Factory(Vec3D.origin)
    rotation: float = 0.0

    def set_rotation(self, degrees: float) -> None:
        """Rotate the node about it's offset until it's angle is `degrees`."""
        self.position = self.position.rotate(
            degrees - rad2deg(self.rotation), around=self.offset
        )
        self.rotation = deg2rad(degrees)

    def rotate(self, degrees: float) -> None:
        """Rotate the node about it's `offset`."""
        self.position = self.position.rotate(degrees, around=self.offset)
        self.rotation += deg2rad(degrees)

    def angle_to(self, point: Vec3D) -> float:
        """Calculate the 2D angle between two nodes."""
        return (point - self.position).normalize().angle_2d()

    def look_at(self, point: Vec3D) -> None:
        """Rotate the node towards a point."""
        self.set_rotation(rad2deg(self.angle_to(point)))


@define
class Circle2D(Node2D):
    """A 2D Circle that can be drawn onto a canvas."""

    radius: float = 10.0
    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.circle(self.position, self.radius, self.color)


@define
class Point2D(Node2D):
    """A 2D point that is drawable on a canvas."""

    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.point(self.position, self.color)


@define
class Line2D(Node2D):
    """A 2D line that is drawable on a canvas."""

    start: Point = Factory(Point.origin)
    end: Point = Factory(Point.origin)
    position: Point = end
    color: Color = color.White
    width: int = 1

    def draw(self, canvas: Canvas) -> None:
        canvas.line(self.start, self.end, self.color, self.width)


@define
class Rect2D(Node2D):
    """A 2D rectangle that is drawable on a canvas."""

    size: Size = Size(20, 20)
    color: Color = color.White

    def draw(self, canvas: Canvas) -> None:
        canvas.rect(self.position, self.size, self.color)


@define
class Polygon2D(Node2D):
    """A 2D polygon that can be drawn on a canvas."""

    lines: list[Point] = Factory(list)
    color: Color = color.White

    def set_rotation(self, degrees: float) -> None:
        self.lines = [
            line.rotate(degrees - rad2deg(self.rotation), around=self.offset)
            for line in self.lines
        ]
        self.rotation = deg2rad(degrees)

    def rotate(self, degrees: float) -> None:
        self.lines = [line.rotate(degrees, around=self.offset) for line in self.lines]
        self.rotation += deg2rad(degrees)

    def draw(self, canvas: Canvas) -> None:
        canvas.polygon(self.lines, self.color)


@define
class BodyInArea(Signal):
    """Emitted while a Node2D is inside an Area2D."""

    emitter: Area2D
    body: Node2D


@define
class OnBodyEntered(Signal):
    """Emitted when a Node2D enters an Area2D."""

    emitter: Area2D
    body: Node2D


@define
class OnBodyExited(Signal):
    """Emitted when a Node2D exits an Area2D."""

    emitter: Area2D
    body: Node2D


# TODO: This is very experiemental and will most definitely be buggy.
# All nodes that emit signals must be defined with eq=False and have their
# __hash__ functions reset.
@define(eq=False)
class Area2D(Node2D):
    """An rectangular area that can detect when a Node2D has entered it."""

    __hash__ = object.__hash__  # type: ignore

    size: Size = Size(20, 20)
    # The list of bodies currently inside the Area2D.
    bodies: list[Node2D] = Factory(list)

    def inside(self, body: Node2D) -> bool:
        """Determine whether a `body` is inside the area."""
        pos: Point = body.position.constrain(self.position, self.position + self.size)
        return pos == body.position

    def tick(self, delta: float, engine: Engine) -> None:
        assert engine.root is not None
        for node in engine.root.world():
            if (
                # Cannot check whether node is inside area if it has no position.
                not isinstance(node, Node2D)
                # Area2D should not detect itself or it's children.
                or node == self
                or node in self.children
                # Area2D should not detect itself or it's children.
                # TODO: This is probably buggy.
                or node == self.parent
                or node in (self.parent.children if self.parent else [])
            ):
                continue
            if self.inside(node):
                BodyInArea(self, node).emit(engine.signals[self])
                if node not in self.bodies:
                    self.bodies.append(node)
                    OnBodyEntered(self, node).emit(engine.signals[self])
            elif node in self.bodies:
                self.bodies.remove(node)
                OnBodyExited(self, node).emit(engine.signals[self])


# TODO: This is very experiemental and will most definitely be buggy.
# Ironically, this is the first node I ever added.
@define
class Label(Node2D):
    """A label with text in it."""

    tag: str = "Label"
    text: str = ""
    color: Color = color.White
    _label: pg.elements.UILabel | None = None

    def __attrs_post_init__(self) -> None:
        self._label = pg.elements.UILabel(
            pygame.Rect(
                self.position.x,
                self.position.y,
                *Font.Monospace.value.size(self.text + "     \n     "),
            ),
            self.text,
            MANAGER,
        )

    def draw(self, canvas: Canvas) -> None:
        assert self._label is not None
        self._label.set_text(self.text)


# TODO: This is very experiemental and will most definitely be buggy.
@define
class Button(Node2D):
    """A clickable button with some text on it."""

    tag: str = "Button"
    text: str = ""
    color: Color = color.White
    _button: pg.elements.UIButton | None = None
    on_click: Callable[[Button], None] | None = None

    def __attrs_post_init__(self) -> None:
        self._button = pg.elements.UIButton(
            pygame.Rect(
                self.position.x,
                self.position.y,
                *Font.Monospace.value.size(self.text + "     \n     "),
            ),
            self.text,
            MANAGER,
        )

    def draw(self, canvas: Canvas) -> None:
        assert self._button is not None
        self._button.set_text(self.text)
        if self._button.check_pressed() and self.on_click is not None:
            self.on_click(self)
