import socket
from _thread import start_new_thread
import pickle
from time import time, sleep
from slack import Game
import traceback

server = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        
        try:
            data = conn.recv(2048*4)

            if gameId in games:
                game = games[gameId]

                game.serverTick()

                if not data:
                    break
                else:
                    game.updateServer(p, data)

                    conn.sendall(pickle.dumps(game.playerData))
            else:
                break
        except Exception:
            traceback.print_exc()
            break

    print("Player Disconnected", gameId, p)

    idCount -= 1
    conn.close()


try:
    while True:
        conn, addr = s.accept()
        print("Listening at:", addr)

        print(idCount)
        p = idCount % 5
        idCount += 1

        print(p)

        gameId = (idCount - 1)//5
        if idCount % 5 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
            start_new_thread(threaded_client, (conn, p, gameId))
        else:
            games[gameId].ready = True
            start_new_thread(threaded_client, (conn, p, gameId))

        games[gameId].newplayer(p)

except KeyboardInterrupt:
    s.close()
    print("Shutdown Server")
