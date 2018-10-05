#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostCreate(TestCase):

    def test_render_host_create_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <host:create xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:create',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })

    def test_render_host_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <host:create xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:addr ip="v4">192.0.2.2</host:addr>
                <host:addr ip="v4">192.0.2.29</host:addr>
                <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
            </host:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:create',
            'name':     'ns1.example1.com',
            'ips': [
                '192.0.2.2',
                '192.0.2.29',
                '1080:0:0:0:8:800:200C:417A'
            ],
            'clTRID':   'XXXX-11',
        })

    def test_parse_host_create_response_success(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'crDate':       '2018-10-05T09:21:37.0Z',
            'name':         'ns1.silverfire.me',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011139311'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <host:creData xmlns:host="urn:ietf:params:xml:ns:host-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                <host:name>ns1.silverfire.me</host:name>
                <host:crDate>2018-10-05T09:21:37.0Z</host:crDate>
            </host:creData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139311</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_host_create_response_fail(self):
        self.assertResponse({
            'clTRID':           'XXXX-11',
            'result_code':      '2005',
            'result_lang':      'en-US',
            'result_msg':       'Parameter value syntax error',
            'result_reason':    '2005:Parameter value syntax error (err.addresses_not_allowed_for_non_child_host:ns1.example1.com)',
            'svTRID':           'SRW-425500000011139320'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="2005">
            <msg lang="en-US">Parameter value syntax error</msg>
            <value xmlns:oxrs="urn:afilias:params:xml:ns:oxrs-1.1">
                <oxrs:xcp>2005:Parameter value syntax error (err.addresses_not_allowed_for_non_child_host:ns1.example1.com)</oxrs:xcp>
            </value>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139320</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
