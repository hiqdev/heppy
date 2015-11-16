import Net
import socket

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

