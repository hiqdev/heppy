import os
import sys
import time
import socket

from pprint import pprint

from heppy.Error import Error
from heppy.Client import Client
from heppy.Request import Request
from heppy.Response import Response

class Daemon:
    @staticmethod
    def start(config, args = {}):
        try:
            client = Client(config['local']['address'])
            client.connect()
        except socket.error as e:
            os.system(config['zdir'] + '/eppyd ' + config['path'] + ' &')
            time.sleep(2)
            client = Client(config['local']['address'])
        if not args.get('login'):
            args['login'] = config['epp']['login']
        if not args.get('pw'):
            args['pw'] = config['epp']['password']
        greeting = client.request('greeting')
        if not greeting:
            Error.die(4, 'failed get greeting')
        greeting = Response.parsexml(greeting)
        pprint(greeting.data)
        if not args.get('objURIs'):
            args['objURIs'] = greeting.get('objURIs')
            for uri in list(args['objURIs']):
                if not uri in Request.modules:
                    del args['objURIs'][uri]
        if not args.get('extURIs'):
            args['extURIs'] = greeting.get('extURIs')
            for uri in list(args['extURIs']):
                if not uri in Request.modules:
                    del args['extURIs'][uri]
        #client = Client(config['local']['address'])
        request = Request.build('epp:login', args)
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
    def stop(config, args = {}):
        Error.die(3, 'failed stop', config)

