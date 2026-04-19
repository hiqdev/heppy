#!/usr/bin/env python

from heppy.Error import Error
from heppy.Request import Request
from heppy.Response import Response


class Logout:

    @staticmethod
    def build(config, args = {}):
        args['command'] = 'epp:logout'
        return Request.build(args)
