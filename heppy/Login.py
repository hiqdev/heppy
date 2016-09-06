#!/usr/bin/env python

from heppy.Error import Error
from heppy.Request import Request
from heppy.Response import Response

class Login:
    @staticmethod
    def build(config, greeting, args = {}):
        if not args.get('login'):
            args['login'] = config['epp']['login']
        if not args.get('pw'):
            args['pw'] = config['epp']['password']
        if not greeting:
            Error.die(4, 'no greeting given')
        greeting = Response.parsexml(greeting)
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
        return Request.build('epp:login', args)
