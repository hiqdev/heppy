#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostCheck(TestCase):

    def test_render_host_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <host:check xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:name>ns2.example2.com</host:name>
                <host:name>ns3.example2.com</host:name>
            </host:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:check',
            'names': [
                'ns1.example1.com',
                'ns2.example2.com',
                'ns3.example2.com',
            ],
            'clTRID':   'XXXX-11',
        })

    def test_parse_host_check_response(self):
        self.assertResponse({
            'avails': {
                'ns1.silverfire.me': '0',
                'ns2.silverfire.me': '0',
                'ns3.silverfire.me': '1'
            },
            'clTRID':       'XXXX-11',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRO-1538732574720'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <host:chkData xmlns:host="urn:ietf:params:xml:ns:host-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                <host:cd>
                    <host:name avail="0">ns1.silverfire.me</host:name>
                </host:cd>
                <host:cd>
                    <host:name avail="0">ns2.silverfire.me</host:name>
                </host:cd>
                <host:cd>
                    <host:name avail="1">ns3.silverfire.me</host:name>
                </host:cd>
            </host:chkData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538732574720</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
