import pyray as pr
from pyray import Vector2, Color
from typing import Optional
from typing import TYPE_CHECKING
from .Shapes import Hexagon
if TYPE_CHECKING:
    from .Entity import Unit


class Tile:
    def __init__(self, x: int, y: int, radius: float,
                 position: Vector2, movementCost: int = 0, bg: str = "Empty") -> None:
        self.x:              int = x
        self.y:              int = y
        self.position:       Vector2 = position
        self.collisionShape: Hexagon = Hexagon(
            position, radius, Color(0, 0, 0, 50)
        )
        self.occupant:       Optional["Unit"] = None
        self.hovered:        bool = False
        self.highlighted:    bool = False
        self.movementCost:   int = movementCost
        self.background:     str = bg

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
