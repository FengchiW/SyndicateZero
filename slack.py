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

    # listens to server for input Server feed
    def updateServer(self, pid, data):
        data = pickle.loads(data)
        if isinstance(data, str):
            if data[:3] == "hit":
                self.playerData[int(data[-1])].hit(5)
                print(self.playerData[int(data[-1])].stats.HITPOINTS)
        else:
            self.playerData[pid] = data

    def connected(self):
        return self.ready
