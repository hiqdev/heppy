# -*- coding: utf-8 -*-

import os
import re
import ssl
import socket
from datetime import datetime

from heppy import Net
from heppy.Config import Config
from heppy.Request import Request
from typing import Union


CLTRID_RE = re.compile(r'<(?:[\w-]+:)?clTRID>\s*(.*?)\s*</(?:[\w-]+:)?clTRID>', re.DOTALL)


def find_cltrid(xml: Union[str, bytes]):
    if isinstance(xml, bytes):
        xml = xml.decode('utf-8', 'replace')
    match = CLTRID_RE.search(xml or '')
    return match.group(1) if match else None


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

    def is_connected(self) -> bool:
        epp = getattr(self, 'epp', None)
        return epp is not None and epp.is_connected()

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
            if self.config.get('insecure_skip_verify') is True:
                # Deliberate, per-registry security downgrade: this server's
                # own certificate is expired (an operational fault on their
                # end, not something a CA bundle or hostname override can
                # fix). Named loudly on purpose - do not set this anywhere
                # except a registry that's actually in this state.
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
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
        # wrap_socket() detaches the plain socket, so closing it alone leaves
        # the TLS connection (and any half-written record) alive: close both.
        for name in ('ssl', 'socket'):
            sock = getattr(self, name, None)
            if sock:
                try:
                    sock.close()
                except OSError:
                    pass
            setattr(self, name, None)

    def is_connected(self) -> bool:
        return getattr(self, 'ssl', None) is not None

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
        reply = self.read()
        self.check_cltrid(xml, reply)
        return reply

    def check_cltrid(self, xml: Union[str, bytes], reply: str) -> None:
        # The server echoes the clTRID it was sent. A different one means this
        # reply belongs to another request (the stream is out of step), so it
        # must not be returned as this request's answer: drop the connection.
        sent = find_cltrid(xml)
        got = find_cltrid(reply)
        if sent is not None and got is not None and got != sent:
            self.disconnect()
            raise ConnectionError('EPP reply clTRID %s does not match request clTRID %s, connection dropped' % (got, sent))

    def write(self, xml: Union[str, bytes]) -> int:
        try:
            return Net.write(self.ssl, xml.decode('utf-8') if isinstance(xml, bytes) else xml)
        except OSError:
            # Timeouts and SSL errors (socket.timeout and ssl.SSLError are
            # OSError) leave the TLS stream in an unknown state - e.g. a
            # partially sent record makes every later write fail with
            # "[SSL: BAD_LENGTH] bad length". Drop the connection instead.
            self.disconnect()
            raise

    def read(self) -> str:
        try:
            return Net.read(self.ssl)
        except OSError:
            self.disconnect()
            raise

