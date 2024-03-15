from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import depict.color as color
import pygame
import pygame_gui as pgui
from attrs import define
from depict.color import Color
from depict.engine import MANAGER
from depict.misc import Font
from depict.nodes import Node2D

if TYPE_CHECKING:
    from depict.canvas import Canvas


# TODO: This is very experimental and will most definitely be buggy.
@define
class Label(Node2D):
    """A label with text in it."""

    tag: str = "Label"
    text: str = ""
    color: Color = color.White
    _label: pgui.elements.UILabel | None = None

    def __attrs_post_init__(self) -> None:
        self._label = pgui.elements.UILabel(
            pygame.Rect(
                self.position.x,
                self.position.y,
                *Font.Monospace.value.size(self.text + "     \n     "),
            ),
            self.text,
            MANAGER,
        )

    def draw(self, canvas: Canvas) -> None:
        assert self._label is not None
        self._label.set_text(self.text)


# TODO: This is very experiemental and will most definitely be buggy.
@define
class Button(Node2D):
    """A clickable button with some text on it."""

    tag: str = "Button"
    text: str = ""
    color: Color = color.White
    _button: pgui.elements.UIButton | None = None
    on_click: Callable[[Button], None] | None = None

    def __attrs_post_init__(self) -> None:
        self._button = pgui.elements.UIButton(
            pygame.Rect(
                self.position.x,
                self.position.y,
                *Font.Monospace.value.size(self.text + "     \n     "),
            ),
            self.text,
            MANAGER,
        )

    def draw(self, canvas: Canvas) -> None:
        assert self._button is not None
        self._button.set_text(self.text)
        if self._button.check_pressed() and self.on_click is not None:
            self.on_click(self)
