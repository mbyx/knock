from __future__ import annotations

"""Monitor and control input devices such as the keyboard and mouse."""

from enum import Enum

import pygame
from attrs import astuple
from depict.vec3d import Point


class MouseButton(Enum):
    """One of the buttons on a mouse."""

    Left = 1
    Middle = 2
    Right = 3
    ScrollUp = 4
    ScrollDown = 5


class Key(Enum):
    """A physical key on a keyboard."""

    def to_str(self) -> str:
        """Convert a `Key` into a `str`."""
        return pygame.key.name(self.value)

    @staticmethod
    def from_str(s: str) -> Key:
        """Create a `Key` from a string."""
        return Key(pygame.key.key_code(s))

    BackSpace = pygame.K_BACKSPACE
    Tab = pygame.K_TAB
    Clear = pygame.K_CLEAR
    Return = pygame.K_RETURN
    Pause = pygame.K_PAUSE
    Escape = pygame.K_ESCAPE
    Space = pygame.K_SPACE
    ExclamationMark = pygame.K_EXCLAIM
    DoubleQuote = pygame.K_QUOTEDBL
    Hash = pygame.K_HASH
    Dollar = pygame.K_DOLLAR
    Ampersand = pygame.K_AMPERSAND
    Quote = pygame.K_QUOTE
    LeftParenthese = pygame.K_LEFTPAREN
    RightParenthese = pygame.K_RIGHTPAREN
    Asterisk = pygame.K_ASTERISK
    Plus = pygame.K_PLUS
    Comma = pygame.K_COMMA
    Minus = pygame.K_MINUS
    Period = pygame.K_PERIOD
    Slash = pygame.K_SLASH
    Num0 = pygame.K_0
    Num1 = pygame.K_1
    Num2 = pygame.K_2
    Num3 = pygame.K_3
    Num4 = pygame.K_4
    Num5 = pygame.K_5
    Num6 = pygame.K_6
    Num7 = pygame.K_7
    Num8 = pygame.K_8
    Num9 = pygame.K_9
    Colon = pygame.K_COLON
    SemiColon = pygame.K_SEMICOLON
    LessThan = pygame.K_LESS
    Equals = pygame.K_EQUALS
    GreaterThan = pygame.K_GREATER
    QuestionMark = pygame.K_QUESTION
    AtSign = pygame.K_AT
    LeftBracket = pygame.K_LEFTBRACKET
    BackSlash = pygame.K_BACKSLASH
    RightBracket = pygame.K_RIGHTBRACKET
    Caret = pygame.K_CARET
    UnderScore = pygame.K_UNDERSCORE
    BackTick = pygame.K_BACKQUOTE
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z
    Delete = pygame.K_DELETE
    Numpad0 = pygame.K_KP0
    Numpad1 = pygame.K_KP1
    Numpad2 = pygame.K_KP2
    Numpad3 = pygame.K_KP3
    Numpad4 = pygame.K_KP4
    Numpad5 = pygame.K_KP5
    Numpad6 = pygame.K_KP6
    Numpad7 = pygame.K_KP7
    Numpad8 = pygame.K_KP8
    Numpad9 = pygame.K_KP9
    NumpadPeriod = pygame.K_KP_PERIOD
    NumpadDivide = pygame.K_KP_DIVIDE
    NumpadMult = pygame.K_KP_MULTIPLY
    NumpadMinus = pygame.K_KP_MINUS
    NumpadPlus = pygame.K_KP_PLUS
    NumpadEnter = pygame.K_KP_ENTER
    NumpadEquals = pygame.K_KP_EQUALS
    Up = pygame.K_UP
    Down = pygame.K_DOWN
    Right = pygame.K_RIGHT
    Left = pygame.K_LEFT
    Insert = pygame.K_INSERT
    Home = pygame.K_HOME
    End = pygame.K_END
    PageUp = pygame.K_PAGEUP
    PageDown = pygame.K_PAGEDOWN
    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12
    F13 = pygame.K_F13
    F14 = pygame.K_F14
    F15 = pygame.K_F15
    NumLock = pygame.K_NUMLOCK
    CapsLock = pygame.K_CAPSLOCK
    ScrollLock = pygame.K_SCROLLOCK
    RShift = pygame.K_RSHIFT
    LShift = pygame.K_LSHIFT
    RCtrl = pygame.K_RCTRL
    LCtrl = pygame.K_LCTRL
    RAlt = pygame.K_RALT
    LAlt = pygame.K_LALT
    RMeta = pygame.K_RMETA
    LMeta = pygame.K_LMETA
    LSuper = pygame.K_LSUPER
    RSuper = pygame.K_RSUPER
    Mode = pygame.K_MODE
    Help = pygame.K_HELP
    Print = pygame.K_PRINT
    SysReq = pygame.K_SYSREQ
    Break = pygame.K_BREAK
    Menu = pygame.K_MENU
    Power = pygame.K_POWER
    Euro = pygame.K_EURO


class Cursor(Enum):
    """The styles a mouse cursor can have."""

    Arrow = pygame.cursors.arrow
    Diamond = pygame.cursors.diamond
    BrokenX = pygame.cursors.broken_x
    TriLeft = pygame.cursors.tri_left
    TriRight = pygame.cursors.tri_right


class Mouse:
    """Methods for manipulating the mouse."""

    @staticmethod
    def set_cursor(cursor: Cursor):
        """Set the mouse cursor to be `cursor`."""
        pygame.mouse.set_cursor(*cursor.value)

    @staticmethod
    def has_focus() -> bool:
        """Check whether the mouse inputs are being fed to the window."""
        return pygame.mouse.get_focused()

    @staticmethod
    def is_visible() -> bool:
        """Check whether the mouse is visible in the window."""
        return pygame.mouse.get_visible()

    @staticmethod
    def set_visible(value: bool):
        """Set whether the mouse is visible in the window."""
        pygame.mouse.set_visible(value)

    @staticmethod
    def set_pos(pos: Point) -> None:
        """Set the position of the mouse cursor."""
        pygame.mouse.set_pos(astuple(pos))

    @staticmethod
    def get_pos() -> Point[int]:
        """Get the position of the mouse cursor."""
        return Point[int](*pygame.mouse.get_pos())

    @staticmethod
    def is_pressed(button: MouseButton) -> bool:
        """Check whether the given mouse `button` is pressed."""
        pygame.event.get()
        buttons = pygame.mouse.get_pressed(num_buttons=5)
        return buttons[button.value - 1]


class Keyboard:
    @staticmethod
    def has_focus() -> bool:
        """Check whether the keyboard inputs are being fed to the window."""
        return pygame.key.get_focused()

    @staticmethod
    def is_pressed(key: Key) -> bool:
        """Check whether the given keyboard `key` is pressed."""
        MODS: dict[Key, int] = {
            Key.LShift: pygame.KMOD_LSHIFT,
            Key.RShift: pygame.KMOD_RSHIFT,
            Key.LCtrl: pygame.KMOD_LCTRL,
            Key.RCtrl: pygame.KMOD_RCTRL,
            Key.LAlt: pygame.KMOD_LALT,
            Key.RAlt: pygame.KMOD_RALT,
            Key.LMeta: pygame.KMOD_LMETA,
            Key.RMeta: pygame.KMOD_RMETA,
            Key.CapsLock: pygame.KMOD_CAPS,
            Key.NumLock: pygame.KMOD_NUM,
        }
        # I do not know what this is. I do not know why I wrote this.
        # All I know is that I won't touch this.
        if key not in MODS:
            return pygame.key.get_pressed()[key.value]
        mask = pygame.key.get_mods()
        return bool(mask & MODS[key])
