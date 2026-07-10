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
        epp = getattr(self, 'epp', None)
        if epp is not None:
            epp.disconnect()

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
        # bound below covers both TCP connect and the TLS handshake, which
        # would otherwise block forever (no OS-level timeout) against a
        # host that's unreachable or silently drops packets.
        self.socket.settimeout(20)
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
            if self.config.get('check_hostname') is False:
                # A handful of registries serve a cert whose CN/SAN doesn't
                # match their EPP hostname (e.g. ZDNS/.top's cert names its
                # host "ZDNS GTLD EPPServer"). The CA chain is still fully
                # verified above; this only skips the hostname/SAN match.
                context.check_hostname = False
            context.load_cert_chain(
                certfile=self.get_path('certfile'),
                keyfile=self.get_path('keyfile')
            )
            self.ssl = context.wrap_socket(self.socket, server_hostname=self.config['host'])

        self.ssl.settimeout(None)
        self.greeting = self.read()
        self.config['start_time'] = datetime.now().isoformat(' ')

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        sock = getattr(self, 'socket', None)
        if sock:
            sock.close()
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
        try:
            return Net.write(self.ssl, xml.decode('utf-8') if isinstance(xml, bytes) else xml)
        except socket.timeout:
            self.disconnect()
            raise

    def read(self) -> str:
        return Net.read(self.ssl)

