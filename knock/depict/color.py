from __future__ import annotations

"""Bright shiny colors."""

import random

import pygame
from attrs import define
import colorsys


@define
class Color:
    """Color of a pixel, in rgb or hsv format.

    Internally, this class stores the color as an rgba value, but can create
    a color from an hsv value."""

    r: int
    g: int
    b: int
    a: int = 255

    @staticmethod
    def hsv(h: int, s: int, v: int) -> Color:
        """Create a color from an hsv value."""
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color.norm(r, g, b)

    @staticmethod
    def norm(r: float, g: float, b: float) -> Color:
        """Create a color from a normalized rgb value.

        Normalized rgb is an rgb value with channels going from 0 to 1 instead
        of 0 to 255."""
        return Color(int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def random(a: int = 255) -> Color:
        """Create a random color, and set its opacity."""
        return Color(
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256),
            a,
        )

    @staticmethod
    def _from_pygame_color(color: pygame.color.Color) -> Color:
        """Convert a `pygame.color.Color` into a `Color`."""
        return Color(color.r, color.g, color.b, color.a)

    def _to_pygame_color(self) -> pygame.color.Color:
        """Convert a `Color` into a `pygame.color.Color`."""
        return pygame.color.Color(self.r, self.g, self.b, self.a)


# Some convenient color constants.
Black: Color = Color(0, 0, 0)
White: Color = Color(255, 255, 255)
Red: Color = Color(255, 0, 0)
Green: Color = Color(0, 255, 0)
Blue: Color = Color(0, 0, 255)
