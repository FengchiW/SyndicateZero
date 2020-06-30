from stats import Status
from math import sqrt


class Bullet:
    def __init__(self, team, x, y, fx, fy, pid="0"):
        self.id = pid
        self.user = team
        self.velocity = 3
        self.range = 300
        self.origin = (x, y)
        self.x = x
        self.y = y
        magnitude = sqrt((int(fx - x) ** 2 + int(fy - y) ** 2))
        self.dir = ((fx - x) / magnitude, (fy - y)/magnitude)

    def update(self):
        self.x += self.velocity * self.dir[0]
        self.y += self.velocity * self.dir[1]


class Player:
    def __init__(self, pid, name="NULL", icon="None"):
        self.id = pid
        self.x = 50
        self.y = 50
        self.velocityX = 0
        self.velocityY = 0
        self.name = name
        self.icon = icon
        self.projectiles = []
        self.stats = Status(100, 100, 0, 50, 50, 0)

    def set_Stats(self, stat_Name, value):
        pass

    def hit(self, damage):
        self.stats.HITPOINTS -= damage

    def update(self):
        if self.x > 0 and self.x < 1200:
            self.x += self.velocityX
            self.velocityX *= 0.8
        else:
            self.velocityX = -abs(self.x)
            self.x = abs(self.x)
        if self.y > 0 and self.y < 800:
            self.y += self.velocityY
            self.velocityY *= 0.8
        else:
            self.y = abs(self.y)

    def move_to_pos(self, loc):
        spd = self.stats.MOVEMENT_SPEED / 25
        if abs(self.velocityY) < self.stats.MOVEMENT_SPEED:
            if loc == 1:
                self.velocityY -= spd
            if loc == 2:
                self.velocityY += spd
        if abs(self.velocityX) < self.stats.MOVEMENT_SPEED:
            if loc == 3:
                self.velocityX -= spd
            if loc == 4:
                self.velocityX += spd
