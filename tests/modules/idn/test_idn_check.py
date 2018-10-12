#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnCheck(TestCase):

    def test_render_idn_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>silverfire.me</domain:name>
            </domain:check>
        </check>
        <extension>
            <idn:check xmlns:idn="urn:afilias:params:xml:ns:idn-1.0">
                <idn:script>de</idn:script>
            </idn:check>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'silverfire.me'
            ],
            'extensions': [
                {
                    'command':  'idn:check',
                    'language': 'de'
                }
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
