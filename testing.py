import time
from threading import Thread, Lock


execRes = "somthing different"
lock = Lock()


def action2():
    global execRes
    while (not lock.acquire(True, 1)):
        execRes = "AI did something!"
        time.sleep(10)
        lock.release()

    print("Failed to get lock!")


def action1():
    global execRes
    if (lock.acquire(True)):
        execRes = "AI did nothing!"
        time.sleep(2)
        lock.release()


def main():
    t = Thread(target=action1, )
    t.start()

    t1 = Thread(target=action2)
    t1.start()

    while (True):
        print(execRes)

        time.sleep(0.1)
    

if __name__ == "__main__":
    main()
