from ..SceneManager import Scene, SceneManager


class IntroScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm)
        sm.rm.load_locales()

    async def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    async def draw(self) -> None:
        super().draw()

    async def handle_input(self) -> None:
        super().handle_input()
