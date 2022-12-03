from typing import Any, Optional
from .Tile import Tile
from pyray import Vector2


tileDirectionNeighbors = [
    [[+1,  0], [+1, -1], [0, -1],
     [-1, -1], [-1,  0], [0, +1]],
    [[+1, +1], [+1,  0], [0, -1],
     [-1,  0], [-1, +1], [0, +1]],
]


class Map:
    def __init__(self, jsonData: dict[str, Any]) -> None:
        self.width: int = jsonData["width"]
        self.height: int = jsonData["height"]
        # TODO: Add a caluclation for the size of the tile radius
        self.tileRadius: float = 40
        self.tiles: list[Tile] = []
        self.tileHeight: float = self.tileRadius * 0.866025
        for i in range(self.height):
            for j in range(self.width):
                self.tiles.append(Tile(
                    j, i,
                    self.tileRadius,
                    Vector2(
                        (j * self.tileRadius) +
                        (j * (self.tileRadius / 2)),
                        (i * 2 * self.tileHeight)
                        + (self.tileHeight * (j % 2))
                    )
                ))

    # TODO: Code the get Neighbors function
    # def getNeighbor(self, tile: Tile, direction: int) -> Optional[Tile]:
    #     parity: int = tile.x & 1
    #     diff = tileDirectionNeighbors[parity][direction]
    #     return self[tile.x + diff[0], tile.y + diff[1]]

    def __getitem__(self, position: tuple[int, int]) -> Optional[Tile]:
        x, y = position[0], position[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.tiles[x + y * self.width]

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self):
        return iter(self.tiles)
