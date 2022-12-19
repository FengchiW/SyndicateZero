from .ResourceManager import ResourceManager
import pyray as pr
from pyray import Color
from typing import Any
from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, sceneManager: 'SceneManager',
                 name: str = "UNKNOWN") -> None:
        self._sm:    'SceneManager' = sceneManager
        self.name:   str = name
        self.isLoaded: bool = False

    @abstractmethod
    def update(self, deltaTime: float) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def onLoad(self) -> None:
        pass

    @abstractmethod
    def handle_input(self) -> None:
        pass

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


class SceneManager:
    def __init__(self) -> None:
        self.scenes:                    list[Scene] = []
        self.consoleMessages:           list[str] = []
        self.shownConsoleMessagesIndex: int = 0
        self.consoleRect:               pr.Rectangle = pr.Rectangle(0, 0, 0, 0)
        self.debug:                     bool = False
        self.shouldExit:                bool = False
        self.rm:                        ResourceManager = ResourceManager(self)
        self.sceneData:                 dict[str, Any] = {}

    def pushScene(self, scene: Scene) -> None:
        self.logMessage(f"Entering {scene}")
        self.scenes.append(scene)

    def popScene(self) -> None:
        if len(self.scenes) > 1:
            self.scenes.pop()
        else:
            exit(0)

    def changeScene(self, scene: Scene) -> None:
        self.scenes = []
        self.scenes.append(scene)
        self.logMessage(f"Changing scene to {scene}")

    def logMessage(self, msg: str, level: int = 0) -> None:
        if level == 0:
            self.consoleMessages.append(f"INFO: {msg}")
        elif level == 1:
            self.consoleMessages.append(f"WARNING: {msg}")
        elif level == 2:
            self.consoleMessages.append(f"ERROR: {msg}")
        else:
            self.consoleMessages.append(f"UNKNOWN: {msg}")

    def drawDebug(self) -> None:
        pr.draw_rectangle_rec(self.consoleRect, Color(0, 0, 0, 200))
        pr.draw_fps(20, 10)
        ci = self.shownConsoleMessagesIndex
        for i, msg in enumerate(self.consoleMessages):
            if (i >= ci and i < ci + 10):
                pr.draw_text(msg, 20, 20 * (i - ci + 1) + 20, 18, Color(150, 255, 255, 255))

    def handleDebugInput(self) -> None:
        if (pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSLASH)):
            sw = pr.get_screen_width()
            sh = pr.get_screen_height()
            self.consoleRect = pr.Rectangle(
                0, 0, sw, sh // 3
            )
            self.debug = not self.debug

        if (self.debug):
            if (pr.is_key_pressed(pr.KeyboardKey.KEY_UP)):
                if (self.shownConsoleMessagesIndex > 0):
                    self.shownConsoleMessagesIndex -= 1
            elif (pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN)):
                if (self.shownConsoleMessagesIndex <
                        len(self.consoleMessages) - 10):
                    self.shownConsoleMessagesIndex += 1

    def run(self) -> None:
        if self.scenes[-1].isLoaded:
            self.update(pr.get_frame_time())
            self.draw()
            self.handle_input()
        self.handleDebugInput()
        if self.debug:
            self.drawDebug()

    def update(self, deltaTime: float) -> None:
        self.scenes[-1].update(deltaTime)

    def draw(self) -> None:
        self.scenes[-1].draw()

    def handle_input(self) -> None:
        self.scenes[-1].handle_input()
