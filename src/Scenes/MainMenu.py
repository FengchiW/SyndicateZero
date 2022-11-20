import pyray as pr

from .LeaderSelect import LeaderSelectScene
from ..SceneManager import Scene, SceneManager
from ..util import Button
from pyray import Color, Vector2


class MainMenu(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm, "MainMenu")
        sm.rm.load_texture("res/background.png", "background")
        self._sm.logMessage("Loaded background texture")
        self.bg = sm.rm.textures["background"]
        width:          int = pr.get_screen_width()
        height:         int = pr.get_screen_height()
        buttonHeight:   int = height // 10
        buttonWidth:    int = width // 4
        buttonY:        int = ((height * 5) // 6) - (buttonHeight//2)

        def getButtonX(i: int) -> int:
            return (width * i // 4) - buttonWidth

        self.buttons: list[Button] = [
            Button(getButtonX(1), buttonY,
                   buttonWidth, buttonHeight, "Solo",
                   lambda: self._sm.changeScene(
                LeaderSelectScene(self._sm)
            )),
            Button(getButtonX(2), buttonY,
                   buttonWidth, buttonHeight, "Multiplayer",
                   None, True),
            Button(getButtonX(3), buttonY,
                   buttonWidth, buttonHeight, "Settings",
                   None, True),
            Button(getButtonX(4), buttonY, buttonWidth, buttonHeight,
                   "Quit", lambda: self._sm.popScene())
        ]

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()
        pr.draw_texture_ex(self.bg, Vector2(0, 0), 0, 1,
                           Color(255, 255, 255, 255))
        for btn in self.buttons:
            btn.draw()

    def handle_input(self) -> None:
        super().handle_input()
        mouse = pr.get_mouse_position()
        for btn in self.buttons:
            btn.handle_input(mouse)
