# -*- coding: utf-8 -*-
import socket

from heppy import Net


class Client:
    def __init__(self, address):
        self.socket = None
        self.address = address

    def _connect(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.settimeout(0.01)
        self.socket.connect(self.address)
        self.socket.settimeout(None)

    def connect(self) -> None:
        if self.socket is None:
            self._connect()

    def disconnect(self) -> None:
        if self.socket:
            self.socket.close()  # Ensure the socket is properly closed
        self.socket = None

    def write(self, data) -> None:
        self.connect()
        Net.write(self.socket, data if isinstance(data, str) else date.encode('utf-8'))

    def read(self) -> str:
        res = Net.read(self.socket)
        self.disconnect()
        return res if isinstance(res, str) else res.decode('utf-8')

    def request(self, data) -> str:
        self.write(data)
        response = self.read()
        return response if isinstance(response , str) else response.decode('utf-8')

    def get_greeting(self) -> str:
        return self.request('greeting')

    @staticmethod
    def try_connect(address) -> bool:
        try:
            client = Client(address)
            client.connect()
            return True
        except (socket.error, OSError):  # Catch specific exceptions
            return False
