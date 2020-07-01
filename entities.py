from stats import Status
from math import sqrt


class Bullet:
    def __init__(self, pid, x, y, fx, fy):
        self.id = pid
        self.origin = (x, y)
        self.x = x
        self.y = y
        magnitude = sqrt((int(fx - x) ** 2 + int(fy - y) ** 2))
        self.dir = ((fx - x) / magnitude, (fy - y)/magnitude)

class Player:
    def __init__(self, pid, name="NULL", icon="None"):
        self.id = pid
        self.x = 50
        self.y = 50
        self.velocityX = 0
        self.velocityY = 0
        self.name = name
        self.icon = icon
        self.shooting = False
        self.lookingAt = (0,0)
        self.stats = Status(100, 100, 0, 50, 50, 0)

    def hit(self, damage):
        self.stats.HITPOINTS -= damage