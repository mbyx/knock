from __future__ import annotations

"""Colors following the Color model."""

import pygame
from attrs import define
import random


@define
class Color:
    """The color of a pixel, with a red, green, and blue channel from 0 to 255."""

    r: int
    g: int
    b: int
    a: int = 255

    @staticmethod
    def random() -> Color:
        return Color(
            random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)
        )

    @staticmethod
    def _from_pygame_color(color: pygame.color.Color) -> Color:
        return Color(color.r, color.g, color.b, color.a)

    def _to_pygame_color(self) -> pygame.color.Color:
        return pygame.color.Color(self.r, self.g, self.b, self.a)


Black: Color = Color(0, 0, 0)
White: Color = Color(255, 255, 255)
Red: Color = Color(255, 0, 0)
Green: Color = Color(0, 255, 0)
Blue: Color = Color(0, 0, 255)
