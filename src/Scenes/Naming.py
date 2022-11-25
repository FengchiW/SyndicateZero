from ..SceneManager import SceneManager, Scene
from ..util import Textbox, Button
from pyray import Vector2, Color
import pyray as pr
from . import MainMenu
from . import Introduction


class NamingScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm)
        self.title:       str = "Good Morning, Commander"
        self.titleLength: int = pr.measure_text(self.title, 50)
        self.width:       int = pr.get_screen_width()
        self.height:      int = pr.get_screen_height()

        self.textbox: Textbox = Textbox(
            Vector2(self.width // 2 - 200, self.height // 2 - 50),
            Vector2(400, 100),
            24,
            12,
            "Enter your name here"
        )

        self.textboxSelected: bool = False

        self.buttons = [
            Button(
                self.width // 2 - 200, self.height // 2 + 100,
                400, 100,
                "Back",
                lambda: self._sm.changeScene(
                    MainMenu.MainMenu(self._sm)
                )
            ),
            Button(
                self.width // 2 - 200, self.height // 2 + 250,
                400, 100,
                "Continue",
                lambda: self.continueToGame()
            )
        ]

    def continueToGame(self):
        self._sm.sceneData["player"]["name"] = self.textbox.text
        self._sm.changeScene(Introduction.IntroScene(self._sm))

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()
        for btn in self.buttons:
            btn.draw()
        self.textbox.draw()
        pr.draw_text(self.title, self.width // 2 - self.titleLength // 2,
                     self.height // 4, 50, Color(50, 50, 50, 255))

    def handle_input(self) -> None:
        super().handle_input()
        mouse = pr.get_mouse_position()
        for btn in self.buttons:
            btn.handle_input(mouse)
        self.textbox.handle_input(mouse)
