from pyray import Vector2, Rectangle, Color
from pyray import draw_rectangle_rec, draw_rectangle_lines_ex


class LoadingBar:
    def __init__(self, position: Vector2, height: float, width: float) -> None:
        self.baseBar: Rectangle = Rectangle(position.x, position.y, width, height)
        self.progressBar: Rectangle = Rectangle(position.x, position.y, 0, height)
        self.progress: int
        self.maxProgress: int

    def setProgress(self, progress: int, maxProgress: int) -> None:
        self.progress = progress
        self.maxProgress = maxProgress
        self.progressBar.width = (self.progress / self.maxProgress) * self.baseBar.width

    def increaseProgress(self, progress: int) -> None:
        self.progress += progress
        self.progressBar.width = (self.progress / self.maxProgress) * self.baseBar.width

    def draw(self) -> None:
        draw_rectangle_rec(self.baseBar, Color(255, 255, 255, 255))
        draw_rectangle_rec(self.progressBar, Color(0, 255, 0, 255))
        draw_rectangle_lines_ex(self.baseBar, 2, Color(0, 0, 0, 255))
        draw_rectangle_lines_ex(self.progressBar, 2, Color(0, 0, 0, 255))

    def reset(self) -> None:
        self.progress = 0
        self.progressBar.width = 0
