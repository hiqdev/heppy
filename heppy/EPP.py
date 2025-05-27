#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import socket
from datetime import datetime

from heppy import Net
from heppy.Config import Config
from heppy.Request import Request
from typing import Union 


class REPP:
    def __init__(self, config):
        self.config = config
        self.connect()

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.epp.disconnect()

    def connect(self):
        self.epp = EPP(self.config)
        self.greeting = self.epp.greeting

    def get_greeting(self) -> str:
        return self.greeting

    def request(self, xml: Union[str, bytes]) -> str:
        res = self.epp.request(xml)
        if not res:
            self.connect()
            res = self.epp.request(xml)
        return res

class EPP:
    def __init__(self, config):
        self.config = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ('bind' in self.config and self.config.get('bind', None) is not None):
            self.socket.bind((self.config['bind'], 0))
        self.socket.connect((self.config['host'], self.config['port']))

        try:
            self.ssl = ssl.wrap_socket(self.socket,
                keyfile  = self.get_path('keyfile'),
                certfile = self.get_path('certfile'),
                ca_certs = self.get_path('ca_certs'),
            )
        except AttributeError:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=self.get_path('ca_certs'))
            context.load_cert_chain(
                certfile=self.get_path('certfile'),
                keyfile=self.get_path('keyfile')
            )
            self.ssl = context.wrap_socket(self.socket, server_hostname=self.config['host'])

        self.greeting = self.read()
        self.config['start_time'] = datetime.now().isoformat(' ')

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        if self.socket:
            self.socket.close()
        self.socket = None

    def get_path(self, name: str) -> str:
        return self.find_path(self.config[name])

    def find_path(self, filename: str) -> str:
        if os.path.isfile(filename):
            return filename
        return self.config['dir'] + '/' + filename

    def get_greeting(self) -> str:
        return self.greeting

    def request(self, xml: Union[str, bytes]) -> str:
        self.write(xml)
        return self.read()

    def write(self, xml: Union[str, bytes]) -> int:
        return Net.write(self.ssl, xml.decode('utf-8') if isinstance(xml, bytes) else xml)

    def read(self) -> str:
        return Net.read(self.ssl)

