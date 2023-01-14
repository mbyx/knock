from attrs import define

from depict import *

from knock.mover import Mover


@define
class Planet(Circle2D):
    position: Point = Point[int](160, 90)
    mass: float = 20.0
    radius: float = (mass**0.5) * 5
    G: float = 9.81

    def force(self, body: Mover) -> Vec3D:
        distance: float = (
            (self.position - body.position).constrain_size(5.0, 10.0).size()
        )
        force: Vec3D = (self.position - body.position).normalize()
        return force * ((self.G * self.mass * body.mass) / (distance**2))

    def attract(self, body: Mover) -> None:
        body.add_force(self.force(body))

    def repel(self, body: Mover) -> None:
        body.add_force(-1 * self.force(body))
