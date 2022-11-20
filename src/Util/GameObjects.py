import pyray as pr
from pyray import Vector2, Color, Rectangle
from typing import Optional
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Entity import Unit


class Tile():
    def __init__(self, x: int, y: int,
                 width: float, height: float, position: Vector2) -> None:
        self.x:          int = x
        self.y:          int = y
        self.rect:       Rectangle = Rectangle(position.x,
                                               position.y,
                                               width, height)
        self.isOccupied: bool = False
        self.occupant:   Optional["Unit"] = None
        self.hovered:    bool = False

    def draw(self) -> None:
        if self.hovered:
            pr.draw_rectangle_rec(self.rect, Color(25, 150, 50, 255))
        else:
            pr.draw_rectangle_rec(self.rect, Color(0, 100, 0, 255))


# returns the number of tiles between two tiles
def distanceBetweenTiles(tile1: Tile, tile2: Tile) -> int:
    return round(abs(tile1.x - tile2.x) ** 2 + abs(tile1.y - tile2.y) ** 2)


# Returns if the summoning was successful
def summonUnit(unit: "Unit", tile: Tile) -> bool:
    if not tile.isOccupied:
        tile.isOccupied = True
        tile.occupant = unit
        unit.rect.x = tile.rect.x
        unit.rect.y = tile.rect.y
        unit.rect.width = tile.rect.width
        unit.rect.height = tile.rect.height
        return True
    else:
        return False
