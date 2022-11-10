from .SceneManager import Scene


class LoadingScene(Scene):
    def __init__(self, sm, resources, nextScene) -> None:
        super().__init__(sm)
        sm.rm.load_resources(resources)

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()

    def handle_input(self) -> None:
        super().handle_input()
