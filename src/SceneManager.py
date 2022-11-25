from .ResourceManager import ResourceManager
import pyray as pr
from typing import Any


class Scene:
    def __init__(self, sceneManager: 'SceneManager',
                 name: str = "UNKNOWN") -> None:
        self._sm:    'SceneManager' = sceneManager
        self.name:   str = name

    def update(self, deltaTime: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def handle_input(self) -> None:
        if (pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSLASH)):
            sw = pr.get_screen_width()
            sh = pr.get_screen_height()
            self._sm.consoleRect = pr.Rectangle(
                0, 0, sw, sh // 3
            )
            self._sm.debug = not self._sm.debug

            if (pr.is_key_pressed(pr.KeyboardKey.KEY_UP)):
                if (self._sm.shownConsoleMessagesIndex > 0):
                    self._sm.shownConsoleMessagesIndex -= 1
            elif (pr.is_key_pressed(pr.KeyboardKey.KEY_DOWN)):
                if (self._sm.shownConsoleMessagesIndex <
                        len(self._sm.consoleMessages) - 10):
                    self._sm.shownConsoleMessagesIndex += 1

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
