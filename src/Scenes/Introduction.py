from ..SceneManager import Scene, SceneManager

class IntroScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm)
        sm.rm.load_locales()
        
    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()

    def handle_input(self) -> None:
        super().handle_input()
