from entities import Enitity


class Game:
    # When the game starts
    def __init__(self, id):
        # Ready Check
        self.ready = False
        # Game ID or Room
        self.id = id
        self.time = None
        # Player objects in game
        self.players = [Enitity("1"), Enitity("2")]
        self.projectiles = []

    def do_game_tick(self, t):
        self.time = t
        for p_id in range(len(self.players)):
            if self.players[p_id] is not None:
                if self.players[p_id].ACTION == "MOVE":
                    self.players[p_id].move_to_pos()

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
            self.players[pid].A_DATA = (int(cmd[2]))

    # ready
    def connected(self):
        return self.ready
