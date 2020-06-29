from stats import Status
import consts

class Enitity:
    def __init__(self, name="NULL", icon="None"):
        self.name = name
        self.icon = icon
        self.stats = Status(0, 0, 0, 50, 0, 0)
        self.ACTION = None
        self.A_DATA = None
        self.ready = False

    def set_Stats(self, stat_Name, value):
        pass

    def move_to_pos(self):
        spd = self.stats.MOVEMENT_SPEED / 25
        loc = self.A_DATA
        if loc is UP:
            self.stats.X_COORD += spd
        
        self.stats.Y_COORD += spd

    def attack_ranged(self, x, y):
        pass

    def attack_melee(self, dir):
        pass
