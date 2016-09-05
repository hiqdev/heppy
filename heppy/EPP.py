#!/usr/bin/env python

import ssl
import socket
from datetime import datetime

from heppy import Net

class REPP:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.epp = EPP(self.config)
        self.greeting = self.epp.greeting

    def command(self, xml):
        res = self.epp.command(xml)
        if not res:
            self.connect()
            res = self.epp.command(xml)
        return res

class EPP:
    def __init__(self, config):
        self.config = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.config['host'], self.config['port']))
        self.ssl = ssl.wrap_socket(self.socket,
            keyfile  = self.config['keyfile'],
            certfile = self.config['certfile'],
            ca_certs = self.config['ca_certs'])
        self.greeting = self.read()
        self.config['start_time'] = datetime.now().isoformat(' ')

    def command(self, xml):
        self.write(xml)
        return self.read()

    def write(self, xml):
        Net.write(self.ssl, xml)

    def read(self):
        return Net.read(self.ssl)


