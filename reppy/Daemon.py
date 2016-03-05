import os
import sys
import time
import socket

from pprint import pprint

from reppy.Error import Error
from reppy.Client import Client
from reppy.Request import Request
from reppy.Response import Response

class Daemon:
    @staticmethod
    def start(config):
        try:
            client = Client(config['local']['address'])
        except socket.error as e:
            os.system(config['zdir'] + '/eppyd ' + config['path'] + ' &')
            time.sleep(2)
            client = Client(config['local']['address'])
        request = Request.build('Login', {
            'login': config['epp']['login'],
            'password': config['epp']['password'],
            #'newPassword': config['epp']['newPassword'],
        })
        query = str(request)
        print Request.prettifyxml(query)
        reply = client.request(query)
        print Request.prettifyxml(reply)
        error = None
        try:
            response = Response.parsexml(reply)
            data = response.data
            pprint(data)
        except Error as e:
            error = e.message
            data = e.data
        if error is not None and data['resultCode']!='2002':
            Error.die(2, 'failed start', data)
        print 'OK'

    @staticmethod
    def stop(config):
        Error.die(3, 'failed stop', config)

