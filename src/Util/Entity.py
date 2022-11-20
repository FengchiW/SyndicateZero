import json
import pyray as pr
from .GameObjects import distanceBetweenTiles, Tile
import math
from pyray import Color
from typing import Optional


class Entity():
    def __init__(self, position: pr.Vector2, width: float, height: float,
                 texture: Optional[pr.Image] = None):
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
    def __init__(self, h: int, a: int, r: int, s: int, ut: str,
                 position: pr.Vector2, width: float, height: float,
                 tile: Tile, p: int):
        super().__init__(position, width, height)
        self.tile:      Tile = tile
        self.health:      int = h
        self.maxHealth:   int = h
        self.attack:      int = a
        self.range:       int = r
        self.speed:       int = s
        self.type:        str = ut
        self.moves:       int = s
        self.player:      int = p
        self.hasAttacked: bool = False

        self.textLength: int = pr.measure_text(self.type, 20)

    def draw(self):
        super().draw()
        color = Color(0, 0, 0, 255)
        if (self.player == 0):
            color = Color(255, 0, 0, 255)
        else:
            color = Color(0, 255, 255, 255)
        pr.draw_rectangle_rec(self.rect, color)
        textX = self.rect.x + (self.rect.width // 2) - self.textLength // 2
        textY = self.rect.y + (self.rect.height // 2) - 10
        pr.draw_text(self.type, int(textX), int(textY), 20,
                     Color(255, 255, 255, 255))

        # Health Text
        pr.draw_text(f"{self.health}/{self.maxHealth}",
                     int(self.rect.x), int(self.rect.y), 20,
                     Color(255, 255, 255, 255))

    def move(self, tile: Tile) -> bool:
        if self.canMoveToTile(tile):
            distance = round(math.sqrt(distanceBetweenTiles(self.tile, tile)))
            self.tile.isOccupied = False
            self.tile.occupant = None
            tile.isOccupied = True
            tile.occupant = self
            self.tile = tile
            self.rect.x = self.tile.rect.x
            self.rect.y = self.tile.rect.y
            self.moves -= distance
            return True
        return False

    def canMoveToTile(self, tile: Tile) -> bool:
        if tile.isOccupied:
            return False
        if (distanceBetweenTiles(self.tile, tile) <= (self.moves ** 2)):
            return True
        return False

    def canAttackUnit(self, unit: 'Unit') -> bool:
        if (distanceBetweenTiles(self.tile, unit.tile) <= (self.attack ** 2)
            and self.player != unit.player
                and not self.hasAttacked):
            return True
        return False

    def attackUnit(self, unit: 'Unit') -> None:
        unit.health -= self.attack
        self.hasAttacked = True

    def update(self):
        super().update()
        self.moves = self.speed
        self.hasAttacked = False


class Card(Entity):
    def __init__(self, cost: int, desc: str = "", name: str = "") -> None:
        self.cost: int = cost
        self.description: str = desc
        self.name: str = name

    def update(self) -> None:
        pass


def get_card_from_json(file: str) -> Optional[Card]:
    try:
        with open(file, "r") as f:
            return Card(json.load(f))
    except FileNotFoundError:
        print("File not found")
        return None
