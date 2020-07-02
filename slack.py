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

    def serverTick(self):
        dead = []
        for i in range(len(self.playerData)):
            if self.playerData[i].stats.HITPOINTS < 0:
                print("dead")
                dead.append(i)
        self.playerData = [self.playerData[pid] for pid in range(len(self.playerData)) if pid not in dead]

    def newplayer(self, pid):
        print("Newplayer")
        self.playerData.append(Player(
                    pid
                ))

    # listens to server for input Server feed
    def updateServer(self, pid, data):
        data = pickle.loads(data)
        if isinstance(data, str):
            if data[:3] == "hit":
                self.playerData[int(data[-1])].hit(5)
        else:
            self.playerData[pid] = data

    def connected(self):
        return self.ready
