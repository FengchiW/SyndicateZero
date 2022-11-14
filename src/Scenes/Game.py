import pyray as pr
from ..SceneManager import SceneManager, Scene
from ..util import Unit, Tile, summonUnit, Button
import math

from pyray import check_collision_point_rec as checkCollision


BOARD_WIDTH = 10
BOARD_HEIGHT = 4


def distanceBetweenTiles(tile1: Tile, tile2: Tile) -> int:
    return abs(tile1.x - tile2.x) ** 2 + abs(tile1.y - tile2.y) ** 2


def canMoveToTile(unit: Unit, tile: Tile) -> bool:
    if tile.isOccupied:
        return False
    if (distanceBetweenTiles(unit.tile, tile) <= (unit.moves ** 2)):
        return True
    return False


def moveUnitToTile(unit: Unit, tile: Tile, prevTile: Tile) -> None:
    movedDistance = round(math.sqrt(distanceBetweenTiles(prevTile, tile)))
    prevTile.isOccupied = False
    prevTile.occupant = None
    tile.isOccupied = True
    tile.occupant = unit
    unit.tile = tile
    unit.moved(movedDistance)


class Game():
    def __init__(self, sw, sh) -> None:
        self.board = []
        self.screenWidth = sw
        self.screenHeight = sh
        self.turn = 0
        self.currentPhase = "Summon"
        self.units: list(Unit) = []
        self.hand = []
        self.graveyard = []
        self.deck = []
        self.selectedUnit = None

        self.endTurnButton = Button(sw - 200, sh - 50, 150, 50, "Next Phase",
                                    lambda: self.endTurn())

        # Create board
        boardViewPortSize: tuple(int, int) = (sw, (sh * 3) // 4)
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                self.board.append(Tile(
                    i, j,
                    boardViewPortSize[0] / BOARD_WIDTH,
                    boardViewPortSize[1] / BOARD_HEIGHT,
                    pr.Vector2(j * (boardViewPortSize[0] / BOARD_WIDTH),
                               i * (boardViewPortSize[1] / BOARD_HEIGHT))
                ))

    def endTurn(self):
        if self.currentPhase == "Summon":
            for unit in self.units:
                if unit.player == 0:
                    unit.moves = 2
            self.currentPhase = "Move"
            self.endTurnButton.text = "End Turn"
        elif self.currentPhase == "Move":
            self.endTurnButton.text = "Waiting..."
            self.currentPhase = "Enemy Summon"
        elif self.currentPhase == "Enemy Summon":
            self.currentPhase = "Enemy Move"
        else:
            self.currentPhase = "Summon"
            self.endTurnButton.text = "Next Phase"
            self.turn += 1

    def drawBoard(self):
        for tile in self.board:
            tile.draw()
        for unit in self.units:
            unit.draw()

        if (self.selectedUnit):
            pr.draw_rectangle_lines(int(self.selectedUnit.rect.x),
                                    int(self.selectedUnit.rect.y),
                                    int(self.selectedUnit.rect.width),
                                    int(self.selectedUnit.rect.height),
                                    (255, 255, 255, 255))

            for tile in self.board:
                if canMoveToTile(self.selectedUnit, tile):
                    pr.draw_rectangle_lines(int(tile.rect.x),
                                            int(tile.rect.y),
                                            int(tile.rect.width),
                                            int(tile.rect.height),
                                            (255, 255, 255, 255))

    def drawUI(self):
        self.endTurnButton.draw()

        # draw the current turn number and phase
        pr.draw_text(f"Turn: {self.turn}",
                     self.screenWidth - 200,
                     self.screenHeight - 90,
                     20, (0, 0, 0, 255))
        pr.draw_text(f"Phase: {self.currentPhase}",
                     self.screenWidth - 200,
                     self.screenHeight - 70,
                     20, (0, 0, 0, 255))

    def update(self, deltaTime: float) -> None:
        mouse = pr.get_mouse_position()
        for tile in self.board:
            tile.hovered = False
            if checkCollision(mouse, tile.rect):
                tile.hovered = True

    def handle_input(self) -> None:
        if self.currentPhase == "Summon":
            mouse = pr.get_mouse_position()
            summoningTiles = [self.board[0], self.board[10],
                              self.board[20], self.board[30]]
            for tile in summoningTiles:
                if checkCollision(mouse, tile.rect):
                    if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                        self.units.append(
                            Unit(4, 1, 2, "warrior",
                                 pr.Vector2(tile.rect.x, tile.rect.y),
                                 tile.rect.width, tile.rect.height, tile, 0))
                        if (not summonUnit(self.units[-1], tile)):
                            self.units.pop()
        else:
            for unit in self.units:
                if checkCollision(pr.get_mouse_position(), unit.rect):
                    if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                        self.selectedUnit = unit
                        break
            if (self.selectedUnit):
                for tile in self.board:
                    if checkCollision(pr.get_mouse_position(), tile.rect):
                        if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                            if canMoveToTile(self.selectedUnit, tile):
                                moveUnitToTile(self.selectedUnit, tile,
                                               self.selectedUnit.tile)
                                self.selectedUnit = None
                                break

        self.endTurnButton.handle_input(pr.get_mouse_position())

    def draw(self):
        self.drawBoard()
        self.drawUI()


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
        self.game.handle_input()
