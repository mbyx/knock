from __future__ import annotations

from attrs import Factory, define

from knock.depict.engine import Engine
from knock.depict.signal import Signal
from knock.depict.vec3d import Point, Size
from knock.depict.nodes import Node2D


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
