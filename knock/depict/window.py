import operator
from enum import IntFlag
from functools import reduce

import pygame
from attrs import define
from depict.vec3d import Size


class Flag(IntFlag):
    """Options to tailor window rendering in depict.

    Configure the rendering behavior with the following options:
    - FullScreen: Display in fullscreen mode.
    - DoubleBuffer: Enable double-buffered rendering.
    - HardwareSurface: Utilize hardware-accelerated surfaces.
    - OpenGL: Create a window with an OpenGL context.
    - Resizable: Allow the window to be resized by the user.
    - NoFrame: Create a borderless window with no frame.
    - Scaled: Enable scaling support for the window.
    - Shown: Make the window initially visible.
    - Hidden: Create the window initially hidden.
    """

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
    """Main window for rendering and drawing.

    Attributes:
        `surface`: The drawing surface of the window.
        `size`: The initial size of the window.
        `flags`: A list of rendering flags to customize the window.

    Methods:
        `tick`: Update the display with new data.
        `is_active`: Check whether the window is currently active.
        `toggle_fullscreen`: Toggle fullscreen mode for this window.
        `set_icon`: Set the icon for this window.
        `set_title`: Set the title for this window.
        `get_size`: Retrieve the current size of the window.

    Note:
        The `size` attribute stores the initial size of the window. If the window
        is resized during runtime, use the `get_size` method to obtain the current size.
    """

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
        pygame.display.flip()

    def is_active(self) -> bool:
        return pygame.display.get_active()

    def toggle_fullscreen(self) -> None:
        pygame.display.toggle_fullscreen()
        self.size = Size(*pygame.display.get_window_size())

    def set_icon(self, surface: pygame.Surface) -> None:
        pygame.display.set_icon(surface)

    def set_title(self, title: str) -> None:
        pygame.display.set_caption(title)

    def get_size(self) -> Size:
        return Size(*pygame.display.get_window_size())
