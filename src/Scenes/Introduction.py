from ..SceneManager import Scene, SceneManager
from ..util import TextBubble, Button
from pyray import Vector2
import pyray as pr
from . import Game


class IntroScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm, "IntroScene")
        # shogun
        self.text = [
            f'Hello, {sm.sceneData["player"]["name"]}. Welcome to the '
            f'world of Shogun. I am your guide, Shogun. I will be '
            f'your guide through this world. I will teach you '
            f'everything you need to know. I will also be your ',
            "Enjoy the game!"
        ]

        self.currentTextIndex: int = 0

        sw: int = int(pr.get_screen_width())
        sh: int = int(pr.get_screen_height())

        self.t: TextBubble = TextBubble(
            Vector2(0, (sh * 4) // 5),
            Vector2(sw, sh//5),
            24,
            self.text[self.currentTextIndex],
            0.001
        )

        self.nextBtn: Button = Button(
            sw - 200, sh - 100,
            200, 100,
            "Next",
            lambda: self.next()
        )

        self.isLoaded = True

    def next(self):
        self.currentTextIndex += 1
        if self.currentTextIndex == len(self.text):
            self._sm.changeScene(Game.GameScene(self._sm))
            return
        self.t.newText(
            self.text[self.currentTextIndex]
        )

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()
        self.t.draw()
        self.nextBtn.draw()

    def handle_input(self) -> None:
        super().handle_input()
        mouse = pr.get_mouse_position()
        self.nextBtn.handle_input(mouse)
