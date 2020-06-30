from entities import Player
import pickle


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
        self.playerData = []

    def newplayer(self, pid):
        print("Newplayer")
        self.playerData.append(Player(
                    pid
                ))

    def do_game_tick(self, t, frame):
        self.time = t
        self.frame = frame

    # listens to server for input Server feed
    def updateServer(self, pid, data):
        if pickle.loads(data) != "ready":
            self.playerData[pid] = pickle.loads(data)

    def connected(self):
        return self.ready
