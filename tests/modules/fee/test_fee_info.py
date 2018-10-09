#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeInfo(TestCase):

    def test_render_fee_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name hosts="all">silverfire.me</domain:name>
            </domain:info>
        </info>
        <extension>
            <fee:info xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:action phase="sunrise">create</fee:action>
                <fee:period unit="y">1</fee:period>
            </fee:info>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command': 'domain:info',
            'name': 'silverfire.me',
            'extensions': [
                {
                    'command':  'fee:info',
                    'name':     'silverfire.me',
                    'action':   'create',
                    'currency': 'USD',
                    'phase':    'sunrise',
                    'period':   1
                },
            ],
            'clTRID': 'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
