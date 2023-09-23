from __future__ import annotations

from collections import defaultdict

"""The main innards of depict."""

from typing import Type, TypeAlias

import pygame
import pygame_gui as pgui
import vidmaker
from attrs import Factory, astuple, define

import depict.color as color
from depict.canvas import Canvas
from depict.color import Color
from depict.misc import Event
from depict.scene import Scene
from depict.signal import Signal, SignalCallback
from depict.vec3d import Size
from depict.window import Window

MANAGER: pgui.UIManager = pgui.UIManager((320, 240))
Clock: TypeAlias = pygame.time.Clock


@define
class Engine:
    """The depict engine.

    This is where you can modify the way depict scenes are run.

    - size: The width and height of the window.
    - title: The title of the window.
    - background: The background color of the window. This is filled every
        tick if `clear` is True.
    - frame_rate: The number of ticks per second.
    - root: The root scene that is drawn to the window.
    - screen: A reference to the window that is created.
    - frame_count: The number of frames that have passed since depict started.
    - record: Whether to record the window or not. This has to be set when
        depict is first run. All subsequent changes will be ignored.
    - clear: Whether to clear the window every tick or not."""

    size: Size
    # Signals are addressed by the Scene instance whose signal you want, and the signal
    # of that scene. This will return a list of subscribers, which are called.
    signals: dict[Scene, dict[Type[Signal], list[SignalCallback]]] = Factory(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    title: str = ""
    background: Color = color.Black
    frame_rate: int = 60
    root: Scene | None = None
    screen: Window | None = None
    frame_count: int = 0
    record: bool = False
    clear: bool = True

    def __attrs_post_init__(self):
        pygame.init()

    @property
    def width(self) -> int:
        return self.size.width

    @property
    def height(self) -> int:
        return self.size.height

    def connect(
        self, callback: SignalCallback, emitter: Scene, signal: Type[Signal]
    ) -> None:
        """Connect a `signal` to be emitted by `emitter` to call `callback`."""
        try:
            self.signals[emitter][signal].append(callback)
        except:
            self.signals[emitter] = {signal: [callback]}

    def run(self, scene: Scene) -> None:
        """Start the depict event loop.

        Creates a window and starts running scenes."""
        self.root = scene

        # If we're recording, create a .mp4 file.
        video: vidmaker.Video | None = None
        if self.record is True:
            # vidmaker.Video has incorrect type annotations...
            video = vidmaker.Video(
                path=f"{scene.tag}.mp4",
                fps=self.frame_rate,  # type: ignore
                resolution=(self.size.width, self.size.height),  # type: ignore
            )

        # Create the window according to the given size.
        screen = Window(size=self.size)
        screen.set_title(self.title if self.title else self.root.__class__.__name__)
        MANAGER.set_window_resolution(astuple(self.size))
        self.screen = screen

        assert screen.surface is not None

        def tick(scene: Scene, delta: float):
            """Update all nodes in a scene recursively."""
            assert screen.surface is not None

            # Run the `draw()` and `tick()` methods of each scene.
            # If the engine has just started, run the `ready()`` method of each scene.
            if delta != 0.0:
                scene.draw(Canvas(screen.surface))
                scene.tick(delta, self)
            else:
                scene.ready(self)

            # Escape recursion if there are no children left.
            if len(scene.children) == 0:
                return

            # Propagate updates down to the children recursively.
            for child in scene.children:
                tick(child, delta)

        tick(scene, delta=0.0)

        # Fill the canvas with a background color before starting.
        with Canvas(screen.surface) as canvas:
            canvas.fill(self.background)

        # Run the event loop indefinitely.
        clock: Clock = Clock()
        try:
            while True:
                # Save the time elapsed since `tick` was called, and increment `frame_count`.
                delta: float = clock.tick(self.frame_rate) / 1000.0
                self.frame_count += 1

                # Handle any queued events.
                for event in Event.get():
                    if event.type == pygame.QUIT:
                        raise KeyboardInterrupt

                    # Pipe the event to the UI Manager.
                    MANAGER.process_events(event)

                # Clear the screen.
                if self.clear is True:
                    with Canvas(screen.surface) as canvas:
                        canvas.fill(self.background)

                # We have initialized the event loop, so we are ready to tick.
                tick(scene, delta)

                # Update the screen in pgui and pygame.
                MANAGER.update(delta)
                MANAGER.draw_ui(screen.surface)
                screen.tick()

                # mypy mistakenly doesn't realize that the `video` is guarded.
                if self.record is True and video is not None:
                    video.update(
                        pygame.surfarray.pixels3d(screen.surface).swapaxes(0, 1),
                    )
        except KeyboardInterrupt:
            # mypy mistakenly doesn't realize that the `video` is guarded.
            if self.record is True and video is not None:
                video.export()
