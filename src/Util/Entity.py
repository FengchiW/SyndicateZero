import json
import pyray as pr


class Entity():
    def __init__(self, position: pr.Vector2, width: float, height: float,
                 texture: pr.Image = None):
        self.rect: pr.Rectangle = pr.Rectangle(position.x, position.y,
                                               width, height)
        self.isHovered: bool = False
        self.isSelectable: bool = False
        self.isSelected: bool = False
        # self.texture: pr.Image = None

    def draw(self):
        pass

    def update(self):
        pass


class Unit(Entity):
    def __init__(self, health: int, attack: int, speed: int, unitType: str,
                 position: pr.Vector2, width: float, height: float,
                 tile, player: int):
        super().__init__(position, width, height)
        self.tile = tile
        self.health:    int = health
        self.maxHealth: int = health
        self.attack:    int = attack
        self.speed:     int = speed
        self.type:      int = unitType
        self.moves:     int = speed
        self.player:    int = 0

        self.textLength: int = pr.measure_text(self.type, 20)

    def draw(self):
        super().draw()
        pr.draw_rectangle_rec(self.rect, (255, 0, 0, 255))
        textX = self.rect.x + (self.rect.width // 2) - self.textLength // 2
        textY = self.rect.y + (self.rect.height // 2) - 10
        pr.draw_text(self.type, int(textX), int(textY), 20,
                     (255, 255, 255, 255))

    def update(self):
        super().update()
        self.moves = self.speed

    def moved(self, distance: int):
        self.rect.x = self.tile.rect.x
        self.rect.y = self.tile.rect.y
        self.moves -= distance


class Card(Entity):
    def __init__(self, cost) -> None:
        pass

    def update():
        pass


def get_card_from_json(file) -> Card:
    try:
        with open(file, "r") as f:
            return Card(json.load(f))
    except FileNotFoundError:
        print("File not found")
        return None


class Player(Unit):
    def __init__(self, id) -> None:
        self.id = id
        self.hand = []
        self.deck = []
        self.graveyard = []
