#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostDelete(TestCase):

    def test_render_host_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <host:delete xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:delete',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })

    def test_parse_host_delete_response_success(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011139652'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139652</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_host_delete_response_failed(self):
        self.assertResponse({
            'clTRID':           'XXXX-11',
            'result_code':      '2303',
            'result_lang':      'en-US',
            'result_msg':       'Object does not exist',
            'result_reason':    'Failed Finding: Host(ns1.example1.com)',
            'svTRID':           'SRW-425500000011139815'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="2303">
            <msg lang="en-US">Object does not exist</msg>
            <value xmlns:oxrs="urn:afilias:params:xml:ns:oxrs-1.1">
                <oxrs:xcp>Failed Finding: Host(ns1.example1.com)</oxrs:xcp>
            </value>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139815</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
