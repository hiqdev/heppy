#!/usr/bin/env python

import os
import json
import time
import socket

from pprint import pprint

from heppy.EPP import REPP
from heppy.Error import Error
from heppy.Login import Login
from heppy.Client import Client
from heppy.Request import Request
from heppy.Systemd import Systemd
from heppy.Response import Response
from heppy.RabbitMQ import RPCServer
from heppy.SignalHandler import SignalHandler

class Daemon:
    def __init__(self, config):
        self.config = config
        self.is_external = False
        self.client = None
        self.handler = SignalHandler({
            'SIGINT':  self.quit,
            'SIGTERM': self.quit,
            'SIGHUP':  self.hello,
            'SIGUSR1': self.hello,
            'SIGUSR2': self.hello,
        })
        self.login_query = None

    def quit(self):
        global quit
        quit()

    def hello(self):
        print "\nHELLO\n"

    def start(self, args = {}):
        self.connect()
        self.login(args)

        rabbit_config = self.config.get('RabbitMQ', {})
        self.server = RPCServer(
            rabbit_config.get('host', 'localhost'),
            rabbit_config.get('queue', 'heppy-' + self.config['name'])
        )
        self.server.connection.add_timeout(5, self.on_timeout)
        self.server.consume(self.smart_request)

    def on_timeout(self):
        self.server.connection.add_timeout(5, self.on_timeout)
        print "\nTIMEOUT\n"

    def systemd(self, args = {}):
        if not 0 in args:
            Error.die(3, 'no systemd command given')

        command = args.pop(0)
        config_path = self.config.abs_path
        bin_path = os.path.abspath(args['zcmd'])
        Systemd(
            name='heppy-' + self.config['name'],
            num=self.config['clientsNum'],
            exec_start="%s %s start" % (bin_path, config_path),
            work_dir=os.path.dirname(config_path)
        ).call(command, args)

    def connect(self):
        if self.client is not None:
            return
        if self.is_external:
            self.connect_external()
        else:
            self.connect_internal()

    def login(self, args = {}):
        try:
            query = self.get_login_query(args)
            print Request.prettifyxml(query)
            reply = self.request(query)
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
        if error is not None and data['result_code'] != '2002':
            Error.die(2, 'bad login response', data)
        print 'LOGIN OK'

    def get_login_query(self, args = {}):
        if self.login_query is None:
            greeting = self.client.get_greeting()
            greetobj = Response.parsexml(greeting)
            pprint(greetobj.data)
            request = Login.build(self.config, greeting, args)
            self.login_query = str(request)
        return self.login_query

    def connect_internal(self):
        config = self.config['epp']
        config['dir'] = self.config.get_dir()
        self.client = REPP(self.config['epp'])

    def connect_external(self):
        try:
            self.client = Client(self.config['local']['address'])
            self.client.connect()
        except socket.error as e:
            os.system(self.config['zdir'] + '/eppyd ' + self.config.path + ' &')
            time.sleep(2)
            self.client = Client(self.config['local']['address'])

    def request(self, query):
        with self.handler.block_signals():
            reply = self.client.request(query)
        return reply

    def smart_request(self, query):
        is_json = query.startswith('{')
        try:
            pass
            if is_json:
                query = self.json2xml(query)
            reply = self.request(query)
            pprint(reply)
            response = Response.parsexml(reply)
            if response.data['result_code'] == '2002':
                response = None
                self.login()
                reply = self.request(query)
            if is_json:
                if not response:
                    response = Response.parsexml(reply)
                reply = json.dumps(response.data)
        except Exception as e:
            if is_json:
                reply = json.dumps({'_error': str(e)})
            else:
                reply = str(e)
        return reply

    def json2xml(self, query):
        request = Request.buildFromDict(json.loads(query))
        return str(request)
