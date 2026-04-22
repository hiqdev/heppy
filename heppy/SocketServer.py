# -*- coding: utf-8 -*-

import json
import os
import socket as socket_module

from heppy import Net


class SocketServer:
    """
    Unix socket RPC server that speaks the same 4-byte length-prefix framing
    protocol as Net.py.  Intended as a lightweight alternative to RabbitMQ
    for direct daemon communication.
    """

    def __init__(self, address: str):
        self.address = address

    def consume(self, handler, recheck=None, check_timeout: float = 30):
        if os.path.exists(self.address):
            os.unlink(self.address)

        dir_name = os.path.dirname(self.address)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        server = socket_module.socket(socket_module.AF_UNIX, socket_module.SOCK_STREAM)
        server.bind(self.address)
        server.listen(5)
        if check_timeout:
            server.settimeout(check_timeout)

        try:
            while True:
                try:
                    conn, _ = server.accept()
                    self._handle(conn, handler)
                    if recheck:
                        recheck()
                except socket_module.timeout:
                    if recheck:
                        recheck()
        finally:
            server.close()
            if os.path.exists(self.address):
                os.unlink(self.address)

    def _handle(self, conn: socket_module.socket, handler) -> None:
        try:
            data = Net.read(conn)
            if not data:
                return
            response = handler(data)
            if isinstance(response, dict):
                response = json.dumps(response)
            if isinstance(response, bytes):
                response = response.decode('utf-8')
            Net.write(conn, response)
        finally:
            conn.close()
