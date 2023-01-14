from __future__ import annotations

"""Miscellaneous methods too small for their own file."""

from enum import Enum
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from depict.color import Color


class Image:
    """Methods for loading and saving an image as a `pygame.surface.Surface`."""

    @staticmethod
    def load(file: str) -> pygame.surface.Surface:
        """Load an image into a `pygame.surface.Surface`."""
        return pygame.image.load(file)

    @staticmethod
    def save(surface: pygame.surface.Surface, file: str):
        """Save a `pygame.surface.Surface` into a `file`."""
        return pygame.image.save(surface, file)


class Time:
    """Methods for working with time."""

    @staticmethod
    def get_ticks() -> int:
        """Get the number of ticks since the animation started."""
        return pygame.time.get_ticks()

    @staticmethod
    def delay(milliseconds: int):
        """Wait for `milliseconds`."""
        pygame.time.delay(milliseconds)

    @staticmethod
    def set_timer(event: pygame.event.Event, milliseconds: int):
        """Emit the `event` after `milliseconds` pass."""
        pygame.time.set_timer(event, milliseconds)


class Font(Enum):
    """Render and load fonts."""

    Monospace = pygame.font.SysFont("monospace", 14)

    @staticmethod
    def get_fonts() -> list[str]:
        """Get a list of all fonts present on the system."""
        return pygame.font.get_fonts()

    def render(self, text: str, fg: Color, bg: Color | None = None) -> pygame.Surface:
        """Render text onto a `pygame.Surface`

        Create a surface with `text` rendered onto it with a foreground and background
        color. If no background color is specified, it defaults to no background."""
        return self.value.render(
            text,
            True,
            fg._to_pygame_color(),
            bg._to_pygame_color() if bg else None,
        )


class Event:
    """Query and manipulate pygame events."""

    @staticmethod
    def get() -> list[pygame.event.Event]:
        """Get a list of events."""
        return pygame.event.get()

    @staticmethod
    def poll() -> pygame.event.Event:
        """Query whether a new event has been emitted."""
        return pygame.event.poll()

    @staticmethod
    def wait() -> pygame.event.Event:
        """Wait until an event has been emitted."""
        return pygame.event.wait()

    @staticmethod
    def clear():
        """Clear all events pending to be processed."""
        pygame.event.clear()

    @staticmethod
    def post(event: pygame.event.Event):
        """Emit an event."""
        return pygame.event.post(event)
