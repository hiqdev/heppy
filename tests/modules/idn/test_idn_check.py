#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnCheck(TestCase):

    def test_render_idn_data_request_for_check(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testfree.test</domain:name>
            </domain:check>
        </check>
        <extension>
            <idn:data xmlns:idn="urn:ietf:params:xml:ns:idn-1.0">
                <idn:table>de</idn:table>
                <idn:table>testfree.test</idn:table>
            </idn:data>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'testfree.test'
            ],
            'extensions': [
                {
                    'command':  'idn',
                    'table':    'de',
                    'name':     'testfree.test',
                }
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
