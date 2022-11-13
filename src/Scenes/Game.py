import pyray as pr
from ..SceneManager import SceneManager, Scene


class Tile():
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.rect = pr.Rectangle(x, y, width, height)
        self.isOccupied = False
        self.occupant = None
        self.hovered = False

    def draw(self) -> None:
        if self.hovered:
            pr.draw_rectangle_rec(self.rect, (50, 255, 150, 255))
        else:
            pr.draw_rectangle_rec(self.rect, (0, 200, 0, 255))


class Game():
    def __init__(self, sw, sh) -> None:
        self.board = []
        self.boardSize = (10, 4)
        self.boardViewPortSize = (sw, (sh * 3) // 4)
        self.screenWidth = sw
        self.screenHeight = sh
        self.turn = 0
        self.currentPhase = 0
        self.players = []

        # Create board
        for i in range(self.boardSize[0]):
            for j in range(self.boardSize[1]):
                self.board.append(Tile(
                    i * (self.boardViewPortSize[0] / self.boardSize[0]),
                    j * (self.boardViewPortSize[1] / self.boardSize[1]),
                    self.boardViewPortSize[0] / self.boardSize[0],
                    self.boardViewPortSize[1] / self.boardSize[1]
                ))

    def drawBoard(self):
        for tile in self.board:
            tile.draw()

    def drawUI(self):
        for i in range(len(self.players[0].hand)):
            pr.draw_rectangle(
                0, i * (self.screenHeight / 10),
                self.screenWidth / 10, self.screenHeight / 10,
                (255, 255, 255, 255)
            )

    def update(self, deltaTime: float) -> None:
        mouse = pr.get_mouse_position()
        for tile in self.board:
            tile.hovered = False
            if pr.check_collision_point_rec(mouse, tile.rect):
                tile.hovered = True

    def draw(self):
        self.drawBoard()


class GameScene(Scene):
    def __init__(self, sm: SceneManager) -> None:
        super().__init__(sm, "Game")
        self.screenWidth = pr.get_screen_width()
        self.screenHeight = pr.get_screen_height()

        self.game = Game(self.screenWidth, self.screenHeight)

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        self.game.update(deltaTime)

    def draw(self) -> None:
        super().draw()
        self.game.draw()

    def handle_input(self) -> None:
        super().handle_input()
