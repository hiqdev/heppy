#!/usr/bin/env python

import ssl
import socket
from datetime import datetime

from heppy import Net
from heppy.Config import Config

class REPP:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.epp = EPP(self.config)
        self.greeting = self.epp.greeting

    def get_greeting(self):
        return self.greeting

    def request(self, xml):
        res = self.epp.request(xml)
        if not res:
            self.connect()
            res = self.epp.request(xml)
        return res

class EPP:
    def __init__(self, config):
        self.config = config
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ('bind' in self.config):
            self.socket.bind((self.config['bind'], 0))
        self.socket.connect((self.config['host'], self.config['port']))
        self.ssl = ssl.wrap_socket(self.socket,
            keyfile  = Config.findFile(self.config['keyfile']),
            certfile = Config.findFile(self.config['certfile']),
            ca_certs = Config.findFile(self.config['ca_certs']),
        )
        self.greeting = self.read()
        self.config['start_time'] = datetime.now().isoformat(' ')

    def get_greeting(self):
        return self.greeting

    def request(self, xml):
        self.write(xml)
        return self.read()

    def write(self, xml):
        Net.write(self.ssl, xml)

    def read(self):
        return Net.read(self.ssl)

