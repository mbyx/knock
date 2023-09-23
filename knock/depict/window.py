import contextlib
import operator
from enum import IntFlag
from functools import reduce

with contextlib.redirect_stdout(None):
    import pygame

from attrs import define
from depict.vec3d import Size


class Flag(IntFlag):
    """Customize how the window will be rendered."""

    FullScreen = pygame.FULLSCREEN
    DoubleBuffer = pygame.DOUBLEBUF
    HardwareSurface = pygame.HWSURFACE
    OpenGL = pygame.OPENGL
    Resizable = pygame.RESIZABLE
    NoFrame = pygame.NOFRAME
    Scaled = pygame.SCALED
    Shown = pygame.SHOWN
    Hidden = pygame.HIDDEN


@define
class Window:
    """The main window in depict."""

    surface: pygame.surface.Surface | None = None
    size: Size = Size(640, 360)
    flags: list[Flag] = []

    def __attrs_post_init__(self) -> None:
        self.surface = pygame.display.set_mode(
            (self.size.width, self.size.height),
            reduce(operator.or_, self.flags, 0),
            vsync=1,
        )

    def tick(self) -> None:
        """Update the display with new data."""
        pygame.display.flip()

    def is_active(self) -> bool:
        """Determine whether the window is active."""
        return pygame.display.get_active()

    def toggle_fullscreen(self) -> None:
        """Turn fullscreen on and off for this window."""
        pygame.display.toggle_fullscreen()

    def set_icon(self, surface: pygame.Surface) -> None:
        """Set the icon of this window."""
        pygame.display.set_icon(surface)

    def set_title(self, title: str) -> None:
        """Set the title for this window."""
        pygame.display.set_caption(title)

    def get_size(self) -> Size:
        """Get the current size of this window.

        If the window was resized, this will return the new size of the window.
        However `Window.size` will store the initial size of the window."""
        return Size(*pygame.display.get_window_size())
