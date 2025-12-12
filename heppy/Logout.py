#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from heppy.Error import Error
from heppy.Request import Request
from heppy.Response import Response


class Logout:

    @staticmethod
    def build(config, args = {}):
        args['command'] = 'epp:logout'
        return Request.build(args)

