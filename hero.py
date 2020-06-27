from stats import Status


class Hero:
    def __init__(self, name="NULL", icon="None"):
        self.name = name
        self.icon = icon
        self.stats = Status(0, 0, 0, 50, 0, 0)
        self.ACTION = None
        self.A_DATA = None

    def move_to(self, x, y):
        pass

    def attact_at(self, x, y):
        pass
