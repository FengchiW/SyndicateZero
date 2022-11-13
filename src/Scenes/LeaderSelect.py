from ..SceneManager import Scene
from ..util import Button
from .Game import GameScene
import pyray as pr


class LeaderSelectScene(Scene):
    def __init__(self, sm) -> None:
        super().__init__(sm)
        self.title: str = "Select a Leader"
        self.titleLength: int = pr.measure_text(self.title, 50)
        self.width: int = pr.get_screen_width()
        self.height: int = pr.get_screen_height()
        buttonHeight: int = self.height * 4 // 5
        buttonWidth: int = self.width // 3 - 25
        buttonY: int = self.height // 6

        def getButtonX(i: int) -> int:
            return ((self.width - 25) * i // 3) - buttonWidth

        self.buttons: list(Button) = [
            Button(getButtonX(1), buttonY, buttonWidth, buttonHeight,
                   "Daddy",
                   lambda: self._sm.changeScene(
                GameScene(self._sm)
            )),
            Button(getButtonX(2), buttonY, buttonWidth, buttonHeight,
                   "Leader 2",
                   lambda: self._sm.changeScene(
                GameScene(self._sm)
            ), True),
            Button(getButtonX(3), buttonY, buttonWidth, buttonHeight,
                   "Leader 3",
                   lambda: self._sm.changeScene(
                GameScene(self._sm)
            ), True),

        ]

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()
        pr.draw_text(self.title, self.width // 2 - self.titleLength // 2,
                     25, 50, (0, 0, 0, 255))
        for btn in self.buttons:
            btn.draw()

    def handle_input(self) -> None:
        super().handle_input()
        mouse = pr.get_mouse_position()
        for btn in self.buttons:
            btn.handle_input(mouse)
