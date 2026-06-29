#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from heppy.Request import Request


class Logout:

    @staticmethod
    def build():
        return Request.build({'command': 'epp:logout'})

