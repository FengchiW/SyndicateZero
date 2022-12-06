from typing import Any, Optional
from .Tile import Tile
from pyray import Vector2


offsets = [[(0, -1), (1, 0), (1, -1), (0, 1), (-1, -1), (-1, 0)],
           [(0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]]


class Map:
    def __init__(self, jsonData: dict[str, Any]) -> None:
        self.width: int = jsonData["map"]["width"]
        self.height: int = jsonData["map"]["height"]
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

    def get_neighbors(self, tile: Tile) -> list[Tile]:
        # Return the neighbors of the hexagon at (x, y)
        neighbors: list[Tile] = []
        for dx, dy in offsets[tile.x % 2]:
            # Check if the neighbor is within the bounds of the grid
            curTile = self[tile.x + dx, tile.y + dy]
            if (curTile is not None):
                if (curTile.movementCost == -1 or curTile.occupant is not None):
                    # The tile is not traversable, so don't
                    continue
                neighbors.append(curTile)
        return neighbors

    def getTilesInMovingRange(self, tile: Tile, distance: int) -> list[tuple[Tile, int]]:
        # Perform a BFS search on the grid to find all hexagons within the given distance from the tile
        queue: list[Tile] = [tile]
        visited = {tile: 0}
        while queue:
            curTile: Tile = queue.pop(0)
            # Add the neighbors of the current hexagon to the queue
            for neighbor in self.get_neighbors(curTile):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = visited[curTile] + 1

        # Return the hexagons that are within the given distance from the start excluding the start
        return [(hexagon, steps) for hexagon, steps in visited.items() if steps <= distance and hexagon != tile]

    def getTilesInRange(self, tile: Tile, distance: int) -> list[tuple[Tile, int]]:
        # Perform a BFS search on the grid to find all hexagons within the given distance from the tile
        queue: list[Tile] = [tile]
        visited = {tile: 0}
        while queue:
            curTile: Tile = queue.pop(0)
            # Add the neighbors of the current hexagon to the queue
            for neighbor in self.get_neighbors(curTile):
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited[neighbor] = visited[curTile] + 1
        # Return the hexagons that are within the given distance from the start
        return [(hexagon, steps) for hexagon, steps in visited.items() if steps <= distance]

    def getDistanceBetweenTiles(self, tile1: Tile, tile2: Tile) -> int:
        return max(abs(tile1.x - tile2.x), abs(tile1.y - tile2.y), abs(tile1.x - tile2.x + tile1.y - tile2.y))

    def __getitem__(self, position: tuple[int, int]) -> Optional[Tile]:
        x, y = position[0], position[1]
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return None
        return self.tiles[x + y * self.width]

    def __len__(self) -> int:
        return self.width * self.height

    def __iter__(self):
        return iter(self.tiles)
