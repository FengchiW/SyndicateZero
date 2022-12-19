from pyray import Vector2, Color
import pyray as pr
import math


class Hexagon:
    def __init__(self, position: Vector2, radius: float, color: Color):
        self.x: float = position.x
        self.y: float = position.y
        self.radius: float = radius
        self.color = color
        self.points: list[Vector2] = []

        for i in range(6):
            self.points.append(Vector2(
                self.x + self.radius * math.cos(2 * math.pi * i / 6),
                self.y + self.radius * math.sin(2 * math.pi * i / 6)
            ))

    def checkCollisionPoint(self, point: Vector2) -> bool:
        def pointInTri(x1: float, y1: float,
                       x2: float, y2: float,
                       x3: float, y3: float,
                       x: float, y: float) -> bool:
            d: float = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
            a: float = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / d
            b: float = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / d
            c: float = 1 - a - b

            return 0 <= a and a <= 1 and 0 <= b and b <= 1 and 0 <= c and c <= 1

        # is the point inside the right triangle?
        if pointInTri(self.points[0].x, self.points[0].y,
                      self.points[1].x, self.points[1].y,
                      self.points[5].x, self.points[5].y,
                      point.x, point.y):
            return True

        # is the point inside the right triangle?
        if pointInTri(self.points[2].x, self.points[2].y,
                      self.points[3].x, self.points[3].y,
                      self.points[4].x, self.points[4].y,
                      point.x, point.y):
            return True

        # is point in the center rectangle?
        if (self.points[2].x <= point.x and point.x <= self.points[1].x and
                self.points[4].y <= point.y and point.y <= self.points[2].y):
            return True
        return False

    def draw(self):
        pr.draw_poly(Vector2(self.x, self.y), 6, self.radius, 90, self.color)
