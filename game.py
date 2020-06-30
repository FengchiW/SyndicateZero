from entities import Enitity, Bullet
from math import sqrt


class Game:
    # When the game starts
    def __init__(self, id):
        # Ready Check
        self.ready = False
        # Game ID or Room
        self.id = id
        self.time = 0
        self.frame = 0
        # Player objects in game
        self.players = [Enitity("1"), Enitity("2")]
        self.projectiles = []

    def do_game_tick(self, t, frame):
        self.time = t
        self.frame = frame
        dead = []
        for bullet in range(len(self.projectiles)):
            curr = self.projectiles[bullet]
            if sqrt((int(curr.x - curr.origin[0]) ** 2 + int(curr.y - curr.origin[1]) ** 2)) < curr.range:
                self.projectiles[bullet].update()
            else:
                dead.append(bullet)
        
        self.projectiles = [(self.projectiles[bullet]) for bullet in range(len(self.projectiles)) if bullet not in dead]

        for p_id in range(len(self.players)):
            if self.players[p_id] is not None:
                self.players[p_id].update()
                if self.players[p_id].ACTION == "MOVE":
                    self.players[p_id].move_to_pos()

    # Function used to get the player positions
    def get_player_details(self, p_id, uname="NULL"):
        # p is player number
        return self.players[p_id]
    
    def get_projectiles(self):
        return self.projectiles

    # listens to server for input Server feed
    def command(self, pid, data):
        # data (BOOL move, ACTION)
        cmd = data.split(",")
        if cmd[0] == "1":
            self.players[pid].ACTION = "MOVE"
            self.players[pid].A_DATA = [(int(cmd[x])) for x in range(1, 5)]
        elif cmd[0] == "2":
            if self.frame % int(500/self.players[pid].stats.DEXTARITY) == 0: 
                self.projectiles.append(Bullet(
                    int(self.players[pid].x),
                    int(self.players[pid].y),
                    int(cmd[1]),
                    int(cmd[2])
                ))

    def connected(self):
        return self.ready
