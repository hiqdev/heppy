#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeCheck(TestCase):

    def test_render_fee_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>silverfire.me</domain:name>
                <domain:name>example.me</domain:name>
                <domain:name>almostempty.me</domain:name>
            </domain:check>
        </check>
        <extension>
            <fee:check xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>silverfire.me</fee:domain>
                <fee:currency>USD</fee:currency>
                <fee:action phase="sunrise">create</fee:action>
                <fee:period unit="y">1</fee:period>
            </fee:check>
            <fee:check xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>example.me</fee:domain>
                <fee:currency>EUR</fee:currency>
                <fee:action phase="claims" subphase="landrush">renew</fee:action>
                <fee:period unit="m">2</fee:period>
            </fee:check>
            <fee:check xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>almostempty.me</fee:domain>
                <fee:action>create</fee:action>
            </fee:check>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command': 'domain:check',
            'names': [
                'silverfire.me',
                'example.me',
                'almostempty.me'
            ],
            'extensions': [
                {
                    'command':  'fee:check',
                    'name':     'silverfire.me',
                    'action':   'create',
                    'currency': 'USD',
                    'phase':    'sunrise',
                    'period':   1
                },
                {
                    'command':  'fee:check',
                    'name':     'example.me',
                    'action':   'renew',
                    'currency': 'EUR',
                    'phase':    'claims',
                    'subphase': 'landrush',
                    'period':   2,
                    'unit':     'm'
                },
                {
                    'command':  'fee:check',
                    'name':     'almostempty.me'
                }
            ],
            'clTRID': 'XXXX-11',
        })

    def test_parse_fee_check_response(self):
        self.assertResponse({
            'avails': {
                'example.com': '1',
                'example.net': '0',
                'example.org': '0'
            },
            'clTRID': 'ABC-12345',
            'reasons': {
                'example.net': 'In use',
                'example.org': 'In use'
            },
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54322-XYZ',
            'extensions': [
                {
                    'action':   'create',
                    'command':  'fee:check',
                    'currency': 'USD',
                    'domain':   'example.com',
                    'fee':      '10.00',
                    'period':   '1',
                    'phase':    'sunrise',
                    'unit':     'y'
                },
                {
                    'action':   'create',
                    'command':  'fee:check',
                    'currency': 'EUR',
                    'domain':   'example.net',
                    'fee':      '5.00',
                    'period':   '2',
                    'phase':    'claims',
                    'subphase': 'landrush',
                    'unit':     'y'
                },
                {
                    'action':   'transfer',
                    'command':  'fee:check',
                    'currency': 'EUR',
                    'domain':   'example.org',
                    'fee':      '2.50',
                    'period':   '2',
                    'unit':     'y'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <resData>
            <domain:chkData
                xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:cd>
                    <domain:name avail="1">example.com</domain:name>
                </domain:cd>
                <domain:cd>
                    <domain:name avail="0">example.net</domain:name>
                    <domain:reason>In use</domain:reason>
                </domain:cd>
                <domain:cd>
                    <domain:name avail="0">example.org</domain:name>
                    <domain:reason>In use</domain:reason>
                </domain:cd>
            </domain:chkData>
        </resData>
        <extension>
            <fee:chkData
                xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>example.com</fee:domain>
                <fee:currency>USD</fee:currency>
                <fee:action phase="sunrise">create</fee:action>
                <fee:period unit="y">1</fee:period>
                <fee:fee>10.00</fee:fee>
            </fee:chkData>
            <fee:chkData
                xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>example.net</fee:domain>
                <fee:currency>EUR</fee:currency>
                <fee:action phase="claims" subphase="landrush">
                create</fee:action>
                <fee:period unit="y">2</fee:period>
                <fee:fee>5.00</fee:fee>
            </fee:chkData>
            <fee:chkData
                xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:domain>example.org</fee:domain>
                <fee:currency>EUR</fee:currency>
                <fee:action>transfer</fee:action>
                <fee:period unit="y">2</fee:period>
                <fee:fee>2.50</fee:fee>
            </fee:chkData>
        </extension>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54322-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
