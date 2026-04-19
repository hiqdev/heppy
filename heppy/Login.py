#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        if not args.get('newPassword'):
            if config['epp'].get("newPassword", None) is not None :
                args['newPassword'] = config['epp']['newPassword']
        if not greeting:
            Error.die(4, 'no greeting given')
        greeting = Response.parsexml(greeting)
        if not args.get('objURIs'):
            args['objURIs'] = greeting.get('objURIs')
            for uri in args['objURIs']:
                if not uri in Request.modules:
                    args['objURIs'].remove(uri)
        if not args.get('extURIs'):
            args['extURIs'] = greeting.get('extURIs')
            for uri in args['extURIs']:
                if not uri in Request.modules:
                    args['extURIs'].remove(uri)
        args['command'] = 'epp:login'
        return Request.build(args)
