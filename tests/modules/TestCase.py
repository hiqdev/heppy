#!/usr/bin/env python

import unittest
from heppy.Request import Request
from heppy.Response import Response


class TestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def assertRequest(self, query, data):
        request = Request.build(data)
        test = Request.prettifyxml(str(request))

        self.assertEqual(query.strip(), test.strip())

    def assertResponse(self, data, reply):
        response = Response.parsexml(reply)
        self.assertDictEqual(data, response.data)

