import socket
from _thread import start_new_thread
import pickle
from time import time, sleep
from game import Game

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


def game_tread(gameId, t):
    while True:
        sleep(120/1000)
        if gameId in games:
            game = games[gameId]
            game.do_game_tick(time()-t)


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    start_new_thread(game_tread, (gameId, time()))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "ready":
                        game.command(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except TypeError:
            print("Uh oh data is wrong type")

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except KeyError:
        "Can't Close Game"
    idCount -= 1
    conn.close()


try:
    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            games[gameId].ready = True
            p = 1

        start_new_thread(threaded_client, (conn, p, gameId))
except KeyboardInterrupt:
    s.close()
    print("Shutdown Server")
