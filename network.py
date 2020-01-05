import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.addr = (None, None)
        self.p = None

    def set_server_address(self, addr):
        if addr is None:
            self.addr = ("172.105.5.44", self.port)
        else:
            self.addr = (addr, self.port)

    def try_connection(self):
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to", self.addr)
            return self.client.recv(2048).decode()
        except ConnectionRefusedError:
            print("Main Server is down Refused!")
            quit()

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)
