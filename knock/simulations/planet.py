"""A planet that can attract or repel objects with mass."""

from attrs import define
from depict import *
from simulations.mover import Mover


@define
class Planet(Mover):
    """A planet that can attract or repel objects with mass."""

    position: Point = Point(160, 90)
    G: float = 6.67 * 10**-11

    def gravitational_force(self, body: Mover, display_scale: float = 1.0) -> Vec3D:
        """The force between two objects with some mass."""
        distance: float = (self.position - body.position).size() / display_scale
        force: Vec3D = (self.position - body.position).normalize()
        return force * ((self.G * self.mass * body.mass) / (distance**2))

    def attract(self, body: Mover, display_scale: float = 1.0) -> None:
        """Attract a body to itself."""
        body.add_force(self.gravitational_force(body, display_scale))

    def repel(self, body: Mover, display_scale: float = 1.0) -> None:
        """Repel a body from itself."""
        body.add_force(-1 * self.gravitational_force(body, display_scale))
