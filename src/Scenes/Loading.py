from ..SceneManager import SceneManager, Scene
from ..ResourceManager import Resource
from ..util import LoadingBar
from pyray import Vector2, get_screen_width
from threading import Thread
import time


class LoadingScene(Scene):
    def __init__(self, sm: SceneManager, resources: list[Resource],
                 nextScene: Scene) -> None:
        super().__init__(sm, "LoadingScene")

        self.loadingBar: LoadingBar = LoadingBar(
            Vector2(0, 0), 50, get_screen_width()
        )

        self.resources = resources
        self.nextScene = nextScene
        self.isLoaded = True

        self.thread = Thread(target=self.loadResources)
        self.thread.start()

    def onLoad(self) -> None:
        super().onLoad()
        self._sm.logMessage("Loading Scene Loaded")

    def loadResources(self) -> None:
        for i, resource in enumerate(self.resources):
            self.loadingBar.setProgress(i, len(self.resources))
            time.sleep(0.1)
            self._sm.rm.load_resource(resource)
        self.nextScene.onLoad()

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        if not self.thread.is_alive():
            self._sm.changeScene(self.nextScene)

    def draw(self) -> None:
        self.loadingBar.draw()
        super().draw()

    def handle_input(self) -> None:
        super().handle_input()
