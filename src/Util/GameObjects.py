import pyray as pr
from pyray import Vector2, Color
from typing import Optional
from typing import TYPE_CHECKING
from .Shapes import Hexagon
if TYPE_CHECKING:
    from .Entity import Unit

tileDirectionNeighbors = [
    [[+1,  0], [+1, -1], [0, -1],
     [-1, -1], [-1,  0], [0, +1]],
    [[+1, +1], [+1,  0], [0, -1],
     [-1,  0], [-1, +1], [0, +1]],
]


class Tile:
    def __init__(self, x: int, y: int,
                 radius: float, position: Vector2) -> None:
        self.x:              int = x
        self.y:              int = y
        self.collisionShape: Hexagon = Hexagon(
            position, radius, Color(0, 0, 0, 50))
        self.occupant:       Optional["Unit"] = None
        self.hovered:        bool = False
        self.highlighted:    bool = False

    def draw(self) -> None:
        if self.hovered:
            # draw tile text
            pr.draw_text(str(self.x) + ", " + str(self.y),
                         int(self.collisionShape.points[0].x),
                         int(self.collisionShape.points[0].y),
                         20, Color(0, 0, 0, 255))

            self.collisionShape.color = Color(255, 255, 255, 100)
        else:
            self.collisionShape.color = Color(0, 0, 0, 50)

        if self.highlighted:
            pr.draw_poly_lines_ex(
                pr.Vector2(self.collisionShape.x,
                           self.collisionShape.y),
                6,
                self.collisionShape.radius,
                90,
                2,
                Color(0, 255, 0, 100)
            )
        self.collisionShape.draw()


class Board:
    def __init__(self, width: int, height: int, tileRadius: float):
        self.width: int = width
        self.height: int = height
        self.tileRadius: float = tileRadius
        self.tiles: list[Tile] = []
        self.tileHeight: float = self.tileRadius * 0.866025
        for i in range(height):
            for j in range(width):
                self.tiles.append(Tile(
                    j, i,
                    self.tileRadius,
                    pr.Vector2(
                        (j * self.tileRadius) +
                        (j * (self.tileRadius / 2)),
                        (i * 2 * self.tileHeight)
                        + (self.tileHeight * (j % 2))
                    )
                ))

    def getNeighbor(self, tile: Tile, direction: int) -> Optional[Tile]:
        parity: int = tile.x & 1
        diff = tileDirectionNeighbors[parity][direction]
        return self[tile.x + diff[0], tile.y + diff[1]]

    def __getitem__(self, position: tuple[int, int]) -> Tile:
        x, y = position[0], position[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            pass
        return self.tiles[x + y * self.width]

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self):
        return iter(self.tiles)


# returns the number of tiles between two tiles
def distanceBetweenTiles(tile1: Tile, tile2: Tile) -> int:
    q1 = tile1.x
    r1 = tile1.y - (tile1.x - (tile1.x & 1)) // 2
    s1 = - q1 - r1

    q2 = tile2.x
    r2 = tile2.y - (tile2.x - (tile2.x & 1)) // 2
    s2 = - q2 - r2

    return max(abs(q1 - q2), abs(r1 - r2), abs(s1 - s2))
