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

    def test_relogin_on_unauthorized_tld(self):
        replies = [self.authorization_error('Unauthorized TLD'), self.GREETING]
        relogins = []
        reply = SmartRequest(self.HELLO_DATA).perform(lambda query: replies.pop(0), lambda: relogins.append(1))
        self.assertEqual(1, len(relogins))
        self.assertEqual({'svID': 'test'}, reply)

    def test_relogin_on_unauthorized_tld_in_msg(self):
        replies = [self.authorization_error(None, 'Authorization error: TLD not authorized'), self.GREETING]
        relogins = []
        reply = SmartRequest(self.HELLO_DATA).perform(lambda query: replies.pop(0), lambda: relogins.append(1))
        self.assertEqual(1, len(relogins))
        self.assertEqual({'svID': 'test'}, reply)

    def test_relogin_only_once_on_unauthorized_tld(self):
        error = self.authorization_error('Unauthorized TLD')
        relogins = []
        reply = SmartRequest(self.HELLO_DATA).perform(lambda query: error, lambda: relogins.append(1))
        self.assertEqual(1, len(relogins))
        self.assertEqual('2201', reply['result_code'])

    def test_no_relogin_on_other_authorization_error(self):
        relogins = []
        for reason in [None, 'Object is not sponsored by you', 'Domain is sponsored by another registrar']:
            error = self.authorization_error(reason)
            reply = SmartRequest(self.HELLO_DATA).perform(lambda query: error, lambda: relogins.append(1))
            self.assertEqual('2201', reply['result_code'])
        self.assertEqual([], relogins)

    def authorization_error(self, reason, msg='Authorization error'):
        ext = ''
        if reason is not None:
            ext = '''
            <extValue>
                <value><text>x</text></value>
                <reason>%s</reason>
            </extValue>''' % reason
        return '''<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="2201">
            <msg>%s</msg>%s
        </result>
        <trID>
            <svTRID>sv-1</svTRID>
        </trID>
    </response>
</epp>''' % (msg, ext)

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
