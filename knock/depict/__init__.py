import pygame

# Required so that we can safely import classes that use Pygame types.
pygame.init()

import depict.utils as utils
from depict.canvas import Canvas
from depict.color import Black, Blue, Color, Green, Red, White
from depict.engine import Engine
from depict.input import Key, Keyboard, Mouse, MouseButton
from depict.misc import Event, Font, Image, Time
from depict.nodes import (
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
from depict.scene import Scene
from depict.signal import Signal, SignalCallback
from depict.vec3d import Point, Size, Vec2D, Vec3D
from depict.window import Window

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
