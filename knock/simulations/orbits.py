"""The Earth and the Moon orbiting each other."""

from attrs import define
from depict import *
from simulations.planet import Planet


@define
class Orbit(Node2D):
    """The Moon orbiting the Earth."""

    # The amount the planets will be scaled by when displayed. However the physics will be accurate.
    # The scaling is only so that it fits on screen.
    display_scale: float = 0.0000012

    def tick(self, delta: float, engine: Engine) -> None:
        if Keyboard.is_pressed(Key.Q):
            exit()

        earth: Planet = self.get_node("Earth")
        moon: Planet = self.get_node("Moon")

        earth.attract(moon, self.display_scale)
        moon.attract(earth, self.display_scale)

    def ready(self, engine: Engine) -> None:
        engine.screen.toggle_fullscreen()

        middle = Point(engine.width // 2, engine.height // 2)

        earth = Planet(
            tag="Earth",
            color=Blue,
            mass=6.0 * 10**24,
            radius=6.38 * 10**6 * self.display_scale,
            position=middle,
        )

        moon = Planet(
            tag="Moon",
            mass=7.35 * 10**22,
            radius=1.74 * 10**6 * self.display_scale,
            color=White,
        )

        moon.position = earth.position + Point(0, 3.84 * 10**8 * self.display_scale)
        moon.velocity.x = 1022.0
        earth.attract(moon, self.display_scale)
        moon.attract(earth, self.display_scale)

        self.children = [
            earth,
            moon,
        ]
