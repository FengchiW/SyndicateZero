from stats import Status


class Enitity:
    def __init__(self, name="NULL", icon="None"):
        self.name = name
        self.icon = icon
        self.stats = Status(0, 0, 0, 50, 0, 0)
        self.ACTION = None
        self.A_DATA = None

    def set_Stats(self, stat_Name, value):
        pass

    def move_to_pos(self):
        spd = self.stats.MOVEMENT_SPEED / 25
        loc = self.A_DATA
        x = self.stats.X_COORD
        y = self.stats.Y_COORD
        if x < loc[0]:
            self.stats.X_COORD += spd
        if y < loc[1]:
            self.stats.Y_COORD += spd
        if x > loc[0]:
            self.stats.X_COORD -= spd
        if y > loc[1]:
            self.stats.Y_COORD -= spd
        if int(x) == int(loc[0]) and int(y) == int(loc[1]):
            self.ACTION = None

    def attack_ranged(self, x, y):
        pass

    def attack_melee(self, dir):
        pass
