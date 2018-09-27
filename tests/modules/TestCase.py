#!/usr/bin/env python

import unittest
from heppy.Request import Request


class TestCase(unittest.TestCase):
    def assertRequest(self, query, data):
        request = Request.buildFromDict(data)
        test = Request.prettifyxml(str(request))

        self.assertEqual(query.strip(), test.strip())
