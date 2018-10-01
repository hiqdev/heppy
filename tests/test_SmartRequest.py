#!/usr/bin/env python

import json
import unittest
from heppy.Request import Request
from heppy.SmartRequest import SmartRequest

class TestSmartRequest(unittest.TestCase):
    def test_get_xml_from_xml(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        request = SmartRequest(xml, self.make_response, self.relogin)
        self.assertEqual(xml, request.get_query())

    def test_get_xml_from_dict(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        request = SmartRequest(data, self.make_response, self.relogin)
        self.assertEqual(xml, request.get_query())

    def test_get_xml_from_json(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        request = SmartRequest(json.dumps(data), self.make_response, self.relogin)
        self.assertEqual(xml, request.get_query())

    def test_perform_xml(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        reply = SmartRequest(xml, self.make_response, self.relogin).perform()
        self.assertEqual(self.make_response(xml), reply)

    def test_perform_dict(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        reply = SmartRequest(data, self.make_response, self.relogin).perform()
        self.assertEqual({'svID': 'test'}, reply)

    def test_perform_json(self):
        data = self.HELLO_DATA
        xml = str(Request.buildFromDict(data))
        reply = SmartRequest(json.dumps(data), self.make_response, self.relogin).perform()
        self.assertEqual('{"svID": "test"}', reply)

    def test_perform_xml_error(self):
        reply = SmartRequest('test', self.raise_error, self.relogin).perform()
        self.assertEqual(self.TEST_ERROR, reply)

    def test_perform_dict_error(self):
        data = self.HELLO_DATA
        reply = SmartRequest(data, self.raise_error, self.relogin).perform()
        self.assertEqual({'_error': self.TEST_ERROR}, reply)

    def test_perform_json_error(self):
        data = self.HELLO_DATA
        reply = SmartRequest(json.dumps(data), self.raise_error, self.relogin).perform()
        self.assertEqual(json.dumps({'_error': self.TEST_ERROR}), reply)


    HELLO_DATA = {'command':  'epp:hello'}

    HELLO = str(Request.buildFromDict(HELLO_DATA))

    GREETING = '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <greeting>
        <svID>test</svID>
    </greeting>
</epp>'''

    def make_response(self, query):
        if query == self.HELLO:
            return self.GREETING
        return 'UNKNOWN QUERY'

    def relogin(self):
        pass

    TEST_ERROR = 'test error'

    def raise_error(self, query):
        raise Exception(self.TEST_ERROR)

if __name__ == '__main__':
    unittest.main()
