#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactCheck(TestCase):

    def test_render_contact_check_request(self):
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


if __name__ == '__main__':
    unittest.main()
