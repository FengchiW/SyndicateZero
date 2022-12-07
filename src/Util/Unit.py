from .Entity import Entity
from .Tile import Tile
from typing import Optional, TYPE_CHECKING
from pyray import Vector2, Rectangle, Color
from pyray import measure_text, draw_text, draw_rectangle_rec, lerp

if TYPE_CHECKING:
    from .Card import Card
    from .Map import Map


class Unit(Entity):
    def __init__(self, health: int, attack: int, unitRange: int,
                 speed: int, unitType: str,
                 position: Vector2, width: float, height: float,
                 tile: Tile, player: int, card: 'Card'):
        super().__init__(position)
        self.tile:        Tile = tile
        self.health:       int = health
        self.maxHealth:    int = health
        self.attack:       int = attack
        self.range:        int = unitRange
        self.speed:        int = speed
        self.type:         str = unitType
        self.moves:        int = speed
        self.player:       int = player
        self.hasAttacked: bool = False
        self.card:      'Card' = card
        self.target:   Vector2 = position
        self.rect:   Rectangle = Rectangle(position.x - width // 2, position.y - height // 2,
                                           width, height)

        self.textLength: int = measure_text(self.type[0], 20)

    def draw(self):
        super().draw()
        color = Color(0, 0, 0, 255)
        if (self.player == 0):
            color = Color(255, 0, 0, 255)
        else:
            color = Color(0, 255, 255, 255)
        draw_rectangle_rec(self.rect, color)
        textX = self.rect.x + (self.rect.width // 2) - self.textLength // 2
        textY = self.rect.y + (self.rect.height // 2) - 10
        draw_text(self.type[0], int(textX), int(textY), 20,
                  Color(255, 255, 255, 255))

        # Health Text
        draw_text(f"{self.health}/{self.maxHealth}",
                  int(self.rect.x), int(self.rect.y), 20,
                  Color(255, 255, 255, 255))

    def move(self, tile: Tile, dist: int) -> None:
        self.tile.occupant = None
        self.tile = tile
        tile.occupant = self
        self.moves -= dist
        self.target = tile.position

    def getLegalMoves(self, board: 'Map') -> list[tuple[Tile, int]]:
        return board.getTilesInMovingRange(self.tile, self.moves)

    def canAttackUnit(self, unit: Optional['Unit'], board: 'Map') -> bool:
        if unit is None:
            return False
        if (board.getTilesInRange(self.tile, self.range).__contains__(unit.tile)
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
            self.rect.x = lerp(self.rect.x, self.target.x - self.rect.width / 2, deltaTime * 10)
            self.rect.y = lerp(self.rect.y, self.target.y - self.rect.height / 2, deltaTime * 10)
