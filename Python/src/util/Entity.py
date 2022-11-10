import json
import pyray as pr


class Entity():
    def __init__(self):
        self.rect = pr.Rectangle(0, 0, 0, 0)
        self.position = pr.Vector2(0, 0)
        self.name = data["name"]
        self.type = data["type"]
        self.attack = data["attack"]
        self.maxHealth = data["health"]
        self.range = data["range"]
        self.movement = data["speed"]
        # self.UnitImage = pr.load_texture(data["image"])
        # self.CardImage = pr.load_texture(data["CardImage"])

    def draw(self):
        pass

    def update(self):
        pass


class Unit(Entity):
    def __init__(self, health, position):
        super().__init__()
        self.health = super.maxHealth
        self.remainingMovement = self.movement

    def draw(self):
        super().draw()

    def update(self):
        super().update()


class Card(Entity):
    def __init__(self, cost) -> None:
        self.cost = cost
        self.description = data["description"]

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
