
class Status:
    def __init__(self, MAX_HP, HP, MP, SPD, X, Y, EFFECTS=[]):
        self.MAX_HITPOINTS = MAX_HP
        self.HITPOINTS = HP
        self.MANA = MP
        self.MAX_MANA = None
        self.MOVEMENT_SPEED = SPD
        self.X_COORD = X
        self.Y_COORD = Y
        self.EFFECTS = EFFECTS
        self.XP = None

    def change_stat(self, stat, value):
        if stat == 'hp':
            self.HITPOINTS = value
        elif stat == 'mhp':
            self.MAX_HITPOINTS = value
        elif stat == 'mp':
            self.MANA = value
        elif stat == 'mmp':
            self.MAX_MANA = value
        elif stat == 'spd':
            self.MOVEMENT_SPEED = value

    def get_current_hp(self):
        return self.HITPOINTS

    def add_effect(self, effect, new):
        pass

    def remove_effect(self, effect, new):
        pass
