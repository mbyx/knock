import pygame

# Required so that we can safely import classes that use Pygame types.
pygame.init()

from knock.depict.nodes import (
    Area2D,
    BodyInArea,
    Button,
    Circle2D,
    Label,
    Line2D,
    Node2D,
    OnBodyEntered,
    OnBodyExited,
    Point2D,
    Polygon2D,
    Rect2D,
)
from knock.depict.canvas import Canvas
from knock.depict.color import Color, Black, White, Blue, Red, Green
from knock.depict.engine import Engine
from knock.depict.input import Key, Keyboard, Mouse, MouseButton
from knock.depict.misc import Event, Font, Image, Time
from knock.depict.scene import Scene
from knock.depict.signal import Signal, SignalCallback
from knock.depict.vec3d import Point, Size, Vec2D, Vec3D
from knock.depict.window import Window
import knock.depict.utils as utils

__all__ = [
    "Node2D",
    "Point2D",
    "Circle2D",
    "Line2D",
    "Rect2D",
    "Polygon2D",
    "Area2D",
    "BodyInArea",
    "OnBodyEntered",
    "OnBodyExited",
    "Label",
    "Button",
    "Canvas",
    "Color",
    "Black",
    "White",
    "Blue",
    "Red",
    "Green",
    "Engine",
    "Key",
    "Keyboard",
    "Mouse",
    "MouseButton",
    "Event",
    "Font",
    "Image",
    "Time",
    "Window",
    "Scene",
    "Signal",
    "SignalCallback",
    "Point",
    "Size",
    "Vec3D",
    "Vec2D",
    "utils",
]
