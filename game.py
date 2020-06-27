from hero import Hero


class Game:
    # When the game starts
    def __init__(self, id):
        # Ready Check
        self.ready = False
        # Game ID or Room
        self.id = id
        self.time = None
        # Player objects in game
        self.players = [Hero("1"), Hero("2")]

    def ready(self):
        pass

    def do_game_tick(self, t):
        self.time = t
        for p_id in range(len(self.players)):
            if self.players[p_id] is not None:
                if self.players[p_id].ACTION == "MOVE":
                    spd = self.players[p_id].stats.MOVEMENT_SPEED / 25
                    loc = self.players[p_id].A_DATA
                    x = self.players[p_id].stats.X_COORD
                    y = self.players[p_id].stats.Y_COORD
                    if x < loc[0]:
                        self.players[p_id].stats.X_COORD += spd
                    if y < loc[1]:
                        self.players[p_id].stats.Y_COORD += spd
                    if x > loc[0]:
                        self.players[p_id].stats.X_COORD -= spd
                    if y > loc[1]:
                        self.players[p_id].stats.Y_COORD -= spd
                    if x == loc[0] and y == loc[1]:
                        self.players[p_id].ACTION = None

    # Function used to get the player positions
    def get_player_details(self, p_id, uname="NULL"):
        # p is player number
        return self.players[p_id]

    # listens to server for input Server feed
    def command(self, pid, data):
        # data (BOOL move, BOOL attack, STR loc)
        cmd = data.split(",")
        # if move command
        print(cmd)
        if cmd[0] == "1":
            self.players[pid].ACTION = "MOVE"
            self.players[pid].A_DATA = (int(cmd[2]), int(cmd[3]))
            print(self.players[pid].ACTION, self.players[pid].A_DATA)
        # if attack command
        if cmd[1] == "1":
            self.players[pid].ACTION = "ATTACK"

    # ready
    def connected(self):
        return self.ready
