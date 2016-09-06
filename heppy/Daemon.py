import os
import sys
import time
import socket

from pprint import pprint

from heppy.EPP import REPP
from heppy.Error import Error
from heppy.Login import Login
from heppy.Client import Client
from heppy.Request import Request
from heppy.Response import Response

class Daemon:
    def __init__(self, config):
        self.config = config
        self.is_external = False
        self.client = None

    def start(self,args = {}):
        self.connect()
        self.login(args)

    def connect(self):
        if self.client is not None:
            return
        if self.is_external:
            self.connect_external()
        else:
            self.connect_internal()

    def login(self, args = {}):
        greeting = self.client.get_greeting()
        greetobj = Response.parsexml(greeting)
        pprint(greetobj.data)
        try:
            request = Login.build(self.config, greeting, args)
            query = str(request)
            print Request.prettifyxml(query)
            reply = self.client.request(query)
            print Request.prettifyxml(reply)
        except Error as e:
            Error.die(2, 'failed perform login request')
        error = None
        try:
            response = Response.parsexml(reply)
            data = response.data
            pprint(data)
        except Error as e:
            error = e.message
            data = e.data
        if error is not None and data['resultCode']!='2002':
            Error.die(2, 'bad login response', data)
        print 'LOGIN OK'

    def connect_internal(self):
        self.client = REPP(self.config['epp'])

    def connect_external(self):
        try:
            self.client = Client(self.config['local']['address'])
            self.client.connect()
        except socket.error as e:
            os.system(self.config['zdir'] + '/eppyd ' + self.config['path'] + ' &')
            time.sleep(2)
            self.client = Client(self.config['local']['address'])

    def stop(args = {}):
        Error.die(3, 'failed stop', config)

