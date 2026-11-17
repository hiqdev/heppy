# -*- coding: utf-8 -*-

import json
import unittest
from heppy.Request import Request
from heppy.SmartRequest import SmartRequest

class TestSmartRequest(unittest.TestCase):
    def test_get_xml_from_xml(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        request = SmartRequest(xml)
        self.assertEqual(xml, request.get_query())

    def test_get_xml_from_dict(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        request = SmartRequest(data)
        self.assertEqual(xml, request.get_query())

    def test_get_xml_from_json(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        request = SmartRequest(json.dumps(data))
        self.assertEqual(xml, request.get_query())

    def test_perform_xml(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        reply = SmartRequest(xml).perform(self.make_response, self.relogin)
        self.assertEqual(self.make_response(xml), reply)

    def test_perform_dict(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        reply = SmartRequest(data).perform(self.make_response, self.relogin)
        self.assertEqual({'svID': 'test'}, reply)

    def test_perform_json(self):
        data = self.HELLO_DATA
        xml = str(Request.build(data))
        reply = SmartRequest(json.dumps(data)).perform(self.make_response, self.relogin)
        self.assertEqual('{"svID": "test"}', reply)

    def test_perform_xml_error(self):
        reply = SmartRequest('test').perform(self.raise_error, self.relogin)
        self.assertEqual(self.TEST_ERROR, reply)

    def test_perform_dict_error(self):
        data = self.HELLO_DATA
        reply = SmartRequest(data).perform(self.raise_error, self.relogin)
        self.assertEqual({'_error': self.TEST_ERROR}, reply)

    def test_perform_json_error(self):
        data = self.HELLO_DATA
        reply = SmartRequest(json.dumps(data)).perform(self.raise_error, self.relogin)
        self.assertEqual(json.dumps({'_error': self.TEST_ERROR}), reply)

    def test_logs_authorization_error(self):
        query = '<epp><command><info><domain:info><domain:name>example.info</domain:name>' \
            '<domain:authInfo><domain:pw>secret</domain:pw></domain:authInfo></domain:info></info></command></epp>'
        reply_xml = self.AUTHORIZATION_ERROR
        with self.assertLogs(level='WARNING') as logs:
            reply = SmartRequest(query).perform(lambda q: reply_xml, self.relogin)
        self.assertEqual(reply_xml, reply)
        self.assertEqual(1, len(logs.output))
        log = logs.output[0]
        self.assertIn('EPP 2201 sv-2201: Authorization error / Unauthorized TLD', log)
        self.assertIn('example.info', log)
        self.assertIn('<domain:pw>***</domain:pw>', log)
        self.assertNotIn('secret', log)
        self.assertIn('<reason>Unauthorized TLD</reason>', log)

    def test_does_not_log_other_replies(self):
        with self.assertNoLogs(level='WARNING'):
            SmartRequest(self.HELLO_DATA).perform(self.make_response, self.relogin)

    AUTHORIZATION_ERROR = '''<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="2201">
            <msg>Authorization error</msg>
            <extValue>
                <value><text>x</text></value>
                <reason>Unauthorized TLD</reason>
            </extValue>
        </result>
        <trID>
            <svTRID>sv-2201</svTRID>
        </trID>
    </response>
</epp>'''

    HELLO_DATA = {'command':  'epp:hello'}

    HELLO = str(Request.build(HELLO_DATA))

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
