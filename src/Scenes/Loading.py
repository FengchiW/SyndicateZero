from ..SceneManager import Scene


class LoadingScene(Scene):
    def __init__(self, sm, resources, nextScene) -> None:
        super().__init__(sm)
        sm.rm.load_resources(resources)

    async def update(self, deltaTime: float) -> None:
        await super().update(deltaTime)

    async def draw(self) -> None:
        await super().draw()

    async def handle_input(self) -> None:
        await super().handle_input()
