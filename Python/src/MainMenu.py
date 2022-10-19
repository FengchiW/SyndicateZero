import pyray as pr

from .Game import GameScene
from .SceneManager import Scene


class Button():
    def __init__(self, x, y, width, height, text, callback) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.callback = callback
        self.isHovered = False

    def draw(self):
        if self.isHovered:
            pr.draw_rectangle(self.x, self.y, self.width,
                              self.height, (255, 255, 255, 255))
            pr.draw_text(self.text, self.x + 10,
                         self.y + 10, 20, (0, 0, 0, 255))
        else:
            pr.draw_rectangle(self.x, self.y, self.width,
                              self.height, (0, 0, 0, 255))
            pr.draw_text(self.text, self.x + 10, self.y +
                         10, 20, (255, 255, 255, 255))

    def is_mouse_over(self, mouse) -> bool:
        if (self.x <= mouse.x <= self.x + self.width
                and self.y <= mouse.y <= self.y + self.height):
            self.isHovered = True
            return True
        self.isHovered = False
        return False

    def handle_input(self, mouse):
        if (self.is_mouse_over(mouse) and
                pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON)):
            self.callback()


class MainMenu(Scene):
    def __init__(self, sm) -> None:
        super().__init__(sm)
        self._sm.consoleMessages.append("MainMenu created")
        self.buttons = [
            Button(100, 100, 200, 50, "Play",
                   lambda: self._sm.changeScene(GameScene(self._sm))),
            Button(100, 200, 200, 50, "Quit", lambda: self._sm.popScene())
        ]

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()
        for btn in self.buttons:
            btn.draw()

    def handle_input(self) -> None:
        super().handle_input()
        mouse = pr.get_mouse_position()
        for btn in self.buttons:
            btn.handle_input(mouse)
