
class Status:
    def __init__(self, MAX_HP, HP, MP, SPD, X, Y, EFFECTS=[]):
        self.MAX_HITPOINTS = MAX_HP
        self.HITPOINTS = HP
        self.MANA = MP
        self.MOVEMENT_SPEED = SPD
        self.X_COORD = X
        self.Y_COORD = Y
        self.EFFECTS = EFFECTS

    def change_stat(self, stat, new):
        pass

    def add_effect(self, effect, new):
        pass

    def remove_effect(self, effect, new):
        pass
