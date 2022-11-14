import pyray as pr
from .Entity import Unit


class Tile():
    def __init__(self, x: int, y: int,
                 width: float, height: float, position: pr.Vector2) -> None:
        self.x: float = x
        self.y: float = y
        self.rect = pr.Rectangle(position.x, position.y, width, height)
        self.isOccupied = False
        self.occupant = None
        self.hovered = False

    def draw(self) -> None:
        if self.hovered:
            pr.draw_rectangle_rec(self.rect, (50, 255, 150, 255))
        else:
            pr.draw_rectangle_rec(self.rect, (0, 200, 0, 255))


# Returns if the summoning was successful
def summonUnit(unit: Unit, tile: Tile) -> bool:
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
