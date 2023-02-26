from __future__ import annotations

from attrs import define
from depict import *

# TODO: Add a simulation runner. A la
# $ knock run flock
# TODO: Make a manual for Depict.
# TODO: Test whether the refactors simulations work.


@define
class Emptiness(Scene):
    pass


Engine(Size(640, 360)).run(Emptiness())
