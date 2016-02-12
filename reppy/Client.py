import socket

from reppy import Net

class Client:
    def __init__(self, address):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.settimeout(0.01)
        self.socket.connect(address)
        self.socket.settimeout(None)

    def write(self, data):
        Net.write(self.socket, data)

    def read(self):
        return Net.read(self.socket)

    def command(self, data):
        self.write(data)
        return self.read()

    @staticmethod
    def try_connect(address):
        try:
            client = Client(address)
            return True
        except:
            return False

