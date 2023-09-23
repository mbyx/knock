from __future__ import annotations

from attrs import Factory, define

import depict.utils as utils
from depict.scene import Scene
from depict.vec3d import Vec3D


@define
class Node2D(Scene):
    """A node with a position and rotation defined around a pivot."""

    # TODO: Add scale.
    position: Vec3D = Factory(Vec3D.origin)
    pivot: Vec3D = Factory(Vec3D.origin)
    _rotation: float = 0.0

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, degrees: float) -> None:
        """Rotate the node about its pivot until its angle is `degrees`."""
        self.position = self.position.rotate(
            degrees - utils.rad2deg(self.rotation), around=self.pivot
        )
        self._rotation = utils.deg2rad(degrees)

    def rotate(self, degrees: float) -> None:
        """Rotate the node about its `pivot`."""
        self.position = self.position.rotate(degrees, around=self.pivot)
        self._rotation += utils.deg2rad(degrees)

    def angle_to(self, point: Vec3D) -> float:
        """Calculate the 2D angle between two nodes."""
        return (point - self.position).normalize().angle_2d()

    def look_at(self, point: Vec3D) -> None:
        """Rotate the node towards a point."""
        self.rotation = utils.rad2deg(self.angle_to(point))
