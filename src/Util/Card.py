from .Entity import Entity
from typing import Any, TYPE_CHECKING
from .Unit import Unit
from pyray import Vector2, Rectangle, Color
from pyray import get_mouse_x, get_mouse_y, draw_rectangle_rec, \
    draw_text, draw_rectangle_lines_ex, check_collision_point_rec

if TYPE_CHECKING:
    from .Tile import Tile


class Card(Entity):
    def __init__(self, cardData: dict[str, Any]) -> None:
        super().__init__(Vector2(0, 0))
        self.unitData: dict[str, Any] = cardData
        self.name: str = self.unitData["name"]
        self.desc: str = self.unitData["desc"]
        self.cost: int = self.unitData["cost"]
        self.isInHand: bool = False
        self.isHeld: bool = False

        self.rect: Rectangle = Rectangle(0, 0, 0, 0)

        self.rectangles: dict[str, Rectangle] = {
            "header": Rectangle(0, 0, 0, 0),
            "body": Rectangle(0, 0, 0, 0),
            "art": Rectangle(0, 0, 0, 0),
        }

    def setPosition(self, x: float, y: float) -> None:
        self.rect.x = x
        self.rect.y = y

    def setSizeForHand(self, sw: float, sh: float):
        self.position.x = self.rect.x
        self.position.y = self.rect.y
        self.rect.width = 175
        self.rect.height = 225

    def update(self, deltaTime: float):
        if self.isInHand:
            self.rectangles["header"] = Rectangle(
                self.rect.x, self.rect.y, self.rect.width,
                self.rect.height * 0.2)
            self.rectangles["body"] = Rectangle(0, 0, 0, 0)
            self.rectangles["art"] = Rectangle(
                self.rect.x,
                self.rect.y + (self.rect.height * 0.2),
                self.rect.width,
                self.rect.height * 0.8)
        if self.isHovered:
            if self.rect.y > self.position.y - 100:
                self.rect.y -= 500 * deltaTime
            if self.rect.width < 200:
                self.rect.width += 100 * deltaTime
            if self.rect.height < 250:
                self.rect.height += 100 * deltaTime
        else:
            self.rect.x = self.position.x
            self.rect.y = self.position.y
            self.rect.width = 175
            self.rect.height = 225

        if self.isHeld:
            self.rect.width = 100
            self.rect.height = 150
            self.rect.x = get_mouse_x() - self.rect.width // 2
            self.rect.y = get_mouse_y() - self.rect.height // 2

    def summonCard(self, tile: "Tile", player: int) -> Unit:
        unit = Unit(self.unitData["health"],
                    self.unitData["attack"],
                    self.unitData["range"],
                    self.unitData["speed"],
                    self.name,
                    Vector2(tile.collisionShape.x, tile.collisionShape.y),
                    tile.collisionShape.radius, tile.collisionShape.radius,
                    tile, player, self)
        tile.occupant = unit
        return unit

    def draw(self) -> None:
        super().draw()
        draw_rectangle_rec(self.rectangles["header"],
                           Color(50, 50, 50, 255))
        draw_rectangle_rec(self.rectangles["art"],
                           Color(100, 100, 100, 255))
        draw_rectangle_rec(self.rectangles["body"],
                           Color(50, 50, 50, 255))
        draw_text(self.name, int(self.rectangles["header"].x + 10),
                  int(self.rectangles["header"].y + 5), 20,
                  Color(255, 255, 255, 255))
        if not self.isInHand:
            draw_text(self.desc, int(self.rectangles["body"].x),
                      int(self.rectangles["body"].y), 20,
                      Color(255, 255, 255, 255))
        if not self.isHeld:
            draw_text(f"{self.cost}",
                      int(self.rectangles["header"].x +
                          self.rectangles["header"].width - 20),
                      int(self.rectangles["header"].y + 5), 20,
                      Color(255, 255, 255, 255))

        if self.isHovered:
            draw_rectangle_rec(self.rect, Color(255, 255, 255, 100))

        draw_rectangle_lines_ex(self.rect, 2, Color(0, 0, 0, 255))

    def is_mouse_over(self, mouse: Vector2) -> bool:
        if (not self.isSelectable):
            return False
        if (check_collision_point_rec(mouse, self.rect)):
            return True
        return False
