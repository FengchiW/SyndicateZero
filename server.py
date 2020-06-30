import socket
from _thread import start_new_thread
import pickle
from time import time, sleep
from game import Game
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


def game_tread(gameId, t):
    frame = 0
    while True:
        frame += 1

        if frame == 120:
            frame = 0

        sleep(1/120)
        if gameId in games:
            game = games[gameId]
            game.do_game_tick(time()-t, frame)


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
        except Exception:
            traceback.print_exc()

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
        print("Listening at:", addr)

        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
            start_new_thread(threaded_client, (conn, p, gameId))
        else:
            games[gameId].ready = True
            p = 1
            start_new_thread(threaded_client, (conn, p, gameId))

except KeyboardInterrupt:
    s.close()
    print("Shutdown Server")
