class Scene:
    def __init__(self, sceneManager) -> None:
        self._sm = sceneManager

    def update(self, deltaTime: float) -> None:
        pass

    def draw(self) -> None:
        pass

    def handle_input(self) -> None:
        pass


class SceneManager:
    def __init__(self) -> None:
        self.scenes = []
        self.consoleMessages = []

    def pushScene(self, scene: Scene) -> None:
        self.scenes.append(scene)

    def popScene(self) -> None:
        if len(self.scenes) > 1:
            self.scenes.pop()
        else:
            exit(0)

    def changeScene(self, scene: Scene) -> None:
        self.scenes = []
        self.scenes.append(scene)
