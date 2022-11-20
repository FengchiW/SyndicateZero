from ..SceneManager import SceneManager, Scene
from ..ResourceManager import Resource


class LoadingScene(Scene):
    def __init__(self, sm: SceneManager, resources: list[Resource],
                 nextScene: Scene) -> None:
        super().__init__(sm)
        # Write loading code here
        sm.changeScene(nextScene)

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)

    def draw(self) -> None:
        super().draw()

    def handle_input(self) -> None:
        super().handle_input()
