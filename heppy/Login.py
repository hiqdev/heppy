# -*- coding: utf-8 -*-

from heppy.Error import Error
from heppy.Request import Request
from heppy.Response import Response


class Login:

    @staticmethod
    def build(config, greeting, args=None):
        args = {} if args is None else args
        if not args.get('login'):
            args['login'] = config['epp']['login']
        if not args.get('pw'):
            args['pw'] = config['epp']['password']
        if not args.get('newPassword'):
            if config['epp'].get('newPassword') is not None:
                args['newPassword'] = config['epp']['newPassword']
        if not greeting:
            Error.die(4, 'no greeting given')
        greeting = Response.parsexml(greeting)
        supported = set(greeting.nsmap.values())
        if not args.get('objURIs'):
            uris = greeting.get('objURIs') or []
            args['objURIs'] = [uri for uri in uris if uri in supported]
        if not args.get('extURIs'):
            uris = greeting.get('extURIs') or []
            args['extURIs'] = [uri for uri in uris if uri in supported]
        args['command'] = 'epp:login'
        return Request.build(args)
