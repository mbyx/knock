from __future__ import annotations

"""A 2D canvas for painting various geometrical shapes."""

import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from attrs import define
from depict.color import Color
from depict.vec3d import Point, Size


@define
class Canvas:
    """A 2D canvas in which to paint."""

    surface: pygame.surface.Surface

    def __enter__(self) -> Canvas:
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        pass

    def point(self, point: Point, color: Color) -> None:
        """Create a point at `point` with a `color`."""
        surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        surface.fill(color._to_pygame_color())
        self.surface.blit(surface, (point.x, point.y))

    def rect(self, point: Point, size: Size, color: Color) -> None:
        """Create a rectangle at `point` with some `size` with a `color`."""
        surface = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
        surface.fill(color._to_pygame_color())
        self.surface.blit(surface, (point.x, point.y))

    def polygon(self, points: list[Point], color: Color) -> None:
        """Create a polygon from a list of `points` with a color."""
        min_point = Point(
            min(map(lambda p: p.x, points)), min(map(lambda p: p.y, points))
        )
        max_point = Point(
            max(map(lambda p: p.x, points)), max(map(lambda p: p.y, points))
        )
        surface = pygame.Surface(max_point.abs_diff(min_point).as_2d(), pygame.SRCALPHA)
        pygame.draw.polygon(
            surface,
            color._to_pygame_color(),
            list(map(lambda point: point.abs_diff(min_point).as_2d(), points)),
        )
        self.surface.blit(surface, min_point.as_2d())

    def circle(self, center: Point, radius: float, color: Color) -> None:
        """Create a circle centered at `center` with a `radius` and `color`."""
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color._to_pygame_color(), (radius, radius), radius)
        self.surface.blit(surface, (center.x - radius, center.y - radius))

    def line(self, start: Point, end: Point, color: Color, width: int = 1) -> None:
        """Draw a line from `start` to `end` with a `color` and `width`."""
        size: Size = Size(
            2 * abs(start.x - end.x) + width, 2 * abs(start.y - end.y) + width
        )
        surface = pygame.Surface((size.width, size.height), pygame.SRCALPHA)

        pygame.draw.line(
            surface,
            color._to_pygame_color(),
            (size.width / 2, size.height / 2),
            ((size.width / 2) + end.x - start.x, (size.height / 2) + end.y - start.y),
            width,
        )
        self.surface.blit(
            surface, (start.x - size.width / 2, start.y - size.height / 2)
        )

    def lines(
        self, points: list[Point], color: Color, is_closed: bool, width: int = 1
    ) -> None:
        """Draw multiple lines at once, and determine whether to fill in the shape."""
        pygame.draw.lines(
            self.surface,
            color._to_pygame_color(),
            is_closed,
            list(map(lambda point: (point.x, point.y), points)),
            width,
        )

    def fill(self, color: Color) -> None:
        """Paint every pixel on the screen the specified `color`."""
        surface = pygame.Surface(
            (self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA
        )
        surface.fill(color._to_pygame_color())
        self.surface.blit(surface, (0, 0))

    def render(self) -> None:
        """Render the changes to the canvas on the screen."""
        pygame.display.flip()
