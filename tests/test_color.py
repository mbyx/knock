import pygame

import knock.depict.color as color
from knock.depict.color import Color


def test_rgb() -> None:
    red: Color = Color(255, 0, 0)
    assert red == color.Red
    assert red.a == 255


def test_color_variants() -> None:
    red: Color = Color(255, 0, 0)
    green: Color = Color(0, 255, 0)
    blue: Color = Color(0, 0, 255)
    black: Color = Color(0, 0, 0)
    white: Color = Color(255, 255, 255)
    assert red == color.Red
    assert green == color.Green
    assert blue == color.Blue
    assert black == color.Black
    assert white == color.White


def test_from_pygame_color() -> None:
    assert color.Red == Color._from_pygame_color(pygame.color.Color(255, 0, 0, 255))


def test_to_pygame_color() -> None:
    assert color.Red._to_pygame_color() == pygame.color.Color(255, 0, 0, 255)


def test_from_pygame_color_and_to_pygame_color_cancel_each_other() -> None:
    assert Color._from_pygame_color(color.Red._to_pygame_color()) == color.Red
