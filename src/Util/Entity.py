import pyray as pr
from .GameObjects import distanceBetweenTiles, Tile
import math
from pyray import Color, Vector2
from typing import Optional, Any


class Entity():
    def __init__(self, position: pr.Vector2, width: float, height: float,
                 texture: Optional[pr.Image] = None):
        self.rect: pr.Rectangle = pr.Rectangle(position.x, position.y,
                                               width, height)
        self.isHovered: bool = False
        self.isSelectable: bool = False
        self.isSelected: bool = False
        # self.texture: pr.Image = None

    def setPosition(self, x: float, y: float) -> None:
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        pass

    def update(self, deltaTime: float) -> None:
        pass


class Unit(Entity):
    def __init__(self, health: int, attack: int, unitRange: int,
                 speed: int, unitType: str,
                 position: pr.Vector2, width: float, height: float,
                 tile: Tile, player: int, card: 'Card'):
        super().__init__(position, width, height)
        self.tile:      Tile = tile
        self.health:      int = health
        self.maxHealth:   int = health
        self.attack:      int = attack
        self.range:       int = unitRange
        self.speed:       int = speed
        self.type:        str = unitType
        self.moves:       int = speed
        self.player:      int = player
        self.hasAttacked: bool = False
        self.card:       'Card' = card
        self.target:    Vector2 = position

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
            self.target = Vector2(tile.rect.x, tile.rect.y)
            self.moves -= distance
            return True
        return False

    def canMoveToTile(self, tile: Tile) -> bool:
        if tile.isOccupied:
            return False
        if (distanceBetweenTiles(self.tile, tile) <= (self.moves ** 2)):
            return True
        return False

    def canAttackUnit(self, unit: Optional['Unit']) -> bool:
        if unit is None:
            return False
        if (distanceBetweenTiles(self.tile, unit.tile) <= (self.attack ** 2)
            and self.player != unit.player
                and not self.hasAttacked):
            return True
        return False

    def attackUnit(self, unit: 'Unit') -> None:
        unit.health -= self.attack
        self.hasAttacked = True

    def reset(self):
        self.hasAttacked = False
        self.moves = self.speed

    def update(self, deltaTime: float) -> None:
        super().update(deltaTime)
        if (self.target.x != self.rect.x or self.target.y != self.rect.y):
            self.rect.x = pr.lerp(self.rect.x, self.target.x, deltaTime * 10)
            self.rect.y = pr.lerp(self.rect.y, self.target.y, deltaTime * 10)


class Card(Entity):
    def __init__(self, cardData: dict[str, Any]) -> None:
        super().__init__(pr.Vector2(0, 0), 0, 0)
        self.unitData: dict[str, Any] = cardData
        self.name: str = self.unitData["name"]
        self.desc: str = self.unitData["desc"]
        self.cost: int = self.unitData["cost"]
        self.isInHand: bool = False
        self.isHeld: bool = False

        self.rectangles: dict[str, pr.Rectangle] = {
            "header": pr.Rectangle(0, 0, 0, 0),
            "body": pr.Rectangle(0, 0, 0, 0),
            "art": pr.Rectangle(0, 0, 0, 0),
        }
        self.originalX = self.rect.x
        self.originalY = self.rect.y

    def setSizeForHand(self, sw: float, sh: float):
        self.originalX = self.rect.x
        self.originalY = self.rect.y
        self.rect.width = 175
        self.rect.height = 225

    def update(self, dt: float):
        if self.isInHand:
            self.rectangles["header"] = pr.Rectangle(
                self.rect.x, self.rect.y, self.rect.width,
                self.rect.height * 0.2)
            self.rectangles["body"] = pr.Rectangle(0, 0, 0, 0)
            self.rectangles["art"] = pr.Rectangle(
                self.rect.x,
                self.rect.y + (self.rect.height * 0.2),
                self.rect.width,
                self.rect.height * 0.8)
        if self.isHovered:
            if self.rect.y > self.originalY - 100:
                self.rect.y -= 500 * dt
            if self.rect.width < 200:
                self.rect.width += 100 * dt
            if self.rect.height < 250:
                self.rect.height += 100 * dt
        else:
            self.rect.x = self.originalX
            self.rect.y = self.originalY
            self.rect.width = 175
            self.rect.height = 225

        if self.isHeld:
            self.rect.width = 100
            self.rect.height = 150
            self.rect.x = pr.get_mouse_x() - self.rect.width // 2
            self.rect.y = pr.get_mouse_y() - self.rect.height // 2

    def summonCard(self, tile: Tile, player: int) -> Unit:
        unit = Unit(self.unitData["health"],
                    self.unitData["attack"],
                    self.unitData["range"],
                    self.unitData["speed"],
                    self.name,
                    pr.Vector2(tile.rect.x, tile.rect.y),
                    tile.rect.width, tile.rect.height,
                    tile, player, self)
        tile.isOccupied = True
        tile.occupant = unit
        return unit

    def draw(self) -> None:
        super().draw()
        pr.draw_rectangle_rec(self.rectangles["header"],
                              Color(50, 50, 50, 255))
        pr.draw_rectangle_rec(self.rectangles["art"],
                              Color(100, 100, 100, 255))
        pr.draw_rectangle_rec(self.rectangles["body"],
                              Color(50, 50, 50, 255))
        pr.draw_text(self.name, int(self.rectangles["header"].x),
                     int(self.rectangles["header"].y), 20,
                     Color(255, 255, 255, 255))
        if not self.isInHand:
            pr.draw_text(self.desc, int(self.rectangles["body"].x),
                         int(self.rectangles["body"].y), 20,
                         Color(255, 255, 255, 255))
        if not self.isHeld:
            pr.draw_text(f"{self.cost}",
                         int(self.rectangles["header"].x +
                             self.rectangles["header"].width - 20),
                         int(self.rectangles["header"].y), 20,
                         Color(255, 255, 255, 255))

        if self.isHovered:
            pr.draw_rectangle_rec(self.rect, Color(255, 255, 255, 100))

    def is_mouse_over(self, mouse: Vector2) -> bool:
        if (not self.isSelectable):
            return False
        if (pr.check_collision_point_rec(mouse, self.rect)):
            return True
        return False
