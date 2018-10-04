#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainCheck(TestCase):

    def test_render_domain_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.me</domain:name>
                <domain:name>silverfire.me</domain:name>
            </domain:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'example.me',
                'silverfire.me',
            ],
            'clTRID':   'XXXX-11',
        })

    def test_parse_domain_check_response(self):
        self.assertResponse({
            'avails': {
                'example.me': '0',
                'silverfire.me': '1'
            },
            'clTRID': 'XXXX-11',
            'reasons': {
                'example.me': 'In use'
            },
            'result_code': '1000',
            'result_lang': 'en-US',
            'result_msg': 'Command completed successfully',
            'svTRID': 'SRO-1538648564538'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                <domain:cd>
                    <domain:name avail="1">silverfire.me</domain:name>
                </domain:cd>
                <domain:cd>
                    <domain:name avail="0">example.me</domain:name>
                    <domain:reason>In use</domain:reason>
                </domain:cd>
            </domain:chkData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538648564538</svTRID>
        </trID>
    </response>
</epp>
''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
