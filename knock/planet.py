"""A planet that can attract or repel objects with mass."""

from attrs import define
from depict import *

from knock.mover import Mover


@define
class Planet(Circle2D):
    """A planet that can attract or repel objects with mass."""

    position: Point = Point(160, 90)
    mass: float = 20.0
    radius: float = (mass**0.5) * 5
    G: float = 9.81

    def gravitational_force(self, body: Mover) -> Vec3D:
        """The force between two objects with some mass."""
        distance: float = (
            (self.position - body.position).constrain_size(5.0, 10.0).size()
        )
        force: Vec3D = (self.position - body.position).normalize()
        return force * ((self.G * self.mass * body.mass) / (distance**2))

    def attract(self, body: Mover) -> None:
        """Attract a body to itself."""
        body.add_force(self.gravitational_force(body))

    def repel(self, body: Mover) -> None:
        """Repel a body from itself."""
        body.add_force(-1 * self.gravitational_force(body))
