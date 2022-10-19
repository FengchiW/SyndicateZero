import pyray as pr
from pyray import check_collision_point_rec as collision
import json

from .SceneManager import Scene

# Constants
SUMMON_PHASE = 0
BATTLE_PHASE = 1
END_PHASE = 2


class Card():
    def __init__(self, data) -> None:
        self.cost = data["cost"]
        self.name = data["name"]
        self.description = data["description"]
        self.type = data["type"]
        self.attack = data["attack"]
        self.maxHealth = data["maxHealth"]
        self.health = data["health"]
        self.range = data["range"]
        self.movement = data["movement"]
        self.remainingMovement = self.movement
        # self.UnitImage = pr.load_texture(data["image"])
        # self.CardImage = pr.load_texture(data["CardImage"])

    def drawAsCard(self) -> None:
        pass

    def drawAsUnit(self) -> None:
        pass


def get_card_from_json(file) -> Card:
    try:
        with open(file, "r") as f:
            return Card(json.load(f))
    except FileNotFoundError:
        print("File not found")
        return None


class Player():
    def __init__(self) -> None:
        self.hand = []
        self.deck = []
        self.units = []
        self.graveyard = []

    def drawCard(self):
        if len(self.deck) > 0:
            self.hand.append(self.deck.pop())

    def summonCard(self, card, x, y):
        pass

    def moveUnit(self, unit, x, y):
        pass

class Tile():
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isOccupied = False
        self.occupant = None
        self.hovered = False

    def draw(self) -> None:
        if self.hovered:
            pr.draw_rectangle(int(self.x), int(self.y),
                              int(self.width), int(self.height),
                              (0, 255, 0, 255))
        else:
            pr.draw_rectangle(int(self.x), int(self.y),
                              int(self.width), int(self.height),
                              (255, 255, 0, 255))


class Game():
    def __init__(self, sw, sh) -> None:
        self.board = []
        self.boardSize = (8, 4)
        self.screenWidth = sw
        self.screenHeight = sh
        self.turn = 0
        self.currentPhase = SUMMON_PHASE
        self.players = []

        for i in range(self.boardSize[0]):
            for j in range(self.boardSize[1]):
                self.board.append(Tile(
                    i * (self.screenWidth / self.boardSize[0]),
                    j * (self.screenHeight / self.boardSize[1]),
                    self.screenWidth / self.boardSize[0],
                    self.screenHeight / self.boardSize[1]
                ))

    def drawBoard(self):
        for tile in self.board:
            tile.draw()

    def drawUI(self):
        pass

    def update(self, deltaTime: float) -> None:
        for tile in self.board:
            # check hover
            tile.hovered = False
            if collision(pr.get_mouse_position(),
                         (tile.x, tile.y, tile.width, tile.height)):
                tile.hovered = True

    def draw(self):
        self.drawBoard()


class GameScene(Scene):
    def __init__(self, sm) -> None:
        super().__init__(sm)
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
