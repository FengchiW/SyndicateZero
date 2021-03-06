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
            self.addr = ("127.0.0.1", self.port)
        else:
            self.addr = (addr, self.port)

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to", self.addr)
            return self.client.recv(2048).decode()
        except ConnectionRefusedError:
            print("Main Server is down Refused!")
            return False
        except socket.gaierror:
            print("Server Doesn't exist")
            return False
    
    def disconect(self):
        try:
            self.client.close()
        except Exception:
            print("An Error Occured")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            rcv = self.client.recv(2048*4)
            return pickle.loads(rcv)
        except socket.error as e:
            print(e)
        except EOFError:
            return None
