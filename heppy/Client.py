import socket

from heppy import Net


class Client:
    def __init__(self, address):
        self.socket  = None
        self.address = address

    def _connect(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.settimeout(0.01)
        self.socket.connect(self.address)
        self.socket.settimeout(None)

    def connect(self):
        if self.socket is None:
            self._connect()

    def disconnect(self):
        self.socket = None

    def write(self, data):
        self.connect()
        Net.write(self.socket, data)

    def read(self):
        res = Net.read(self.socket)
        self.disconnect()
        return res

    def request(self, data):
        self.write(data)
        return self.read()

    def get_greeting(self):
        return self.request('greeting')

    @staticmethod
    def try_connect(address):
        try:
            client = Client(address)
            client.connect()
            return True
        except:
            return False

