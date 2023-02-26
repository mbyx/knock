"""A viscous liquid that applies a drag force on objects."""

from typing import cast

from attrs import define
from depict import *

from knock.mover import Mover


@define
class Liquid(Rect2D):
    """A viscous liquid that applies a drag force on objects."""

    # Cover half the screen.
    position: Point = Point(0, 180)
    size: Size = Size(640, 180)

    drag: float = 0.15

    def body_in_area(self, emitter: Area2D, body: Node2D) -> None:
        """Called whenever a body is inside the liquid."""
        if isinstance(body, Mover):
            drag: Vec3D = (
                -1 * (body.velocity.size() ** 2) * self.drag * body.velocity.normalize()
            )
            body.add_force(drag)

    def build(self) -> list[Scene]:
        return [
            # Specifying the parent node is optional in depict, as a good node
            # should almost always be unaware of anything besides itself and its
            # children.
            # However, Area2D needs to check whether the Node2D inside it isn't the
            # parent or the parent's children.
            Area2D(tag="Detector", position=self.position, size=self.size, parent=self)
        ]

    def ready(self, engine: Engine) -> None:
        detector: Area2D = cast(Area2D, self.get_node("Detector"))
        engine.connect(self.body_in_area, detector, BodyInArea)
