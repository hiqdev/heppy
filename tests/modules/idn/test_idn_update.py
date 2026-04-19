#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnUpdate(TestCase):

    def test_render_idn_data_request_for_update(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:chg/>
            </domain:update>
        </update>
        <extension>
            <idn:data xmlns:idn="urn:ietf:params:xml:ns:idn-1.0">
                <idn:table>fr</idn:table>
                <idn:table>testdomain.test</idn:table>
            </idn:data>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':  'domain:update',
            'name':     'testdomain.test',
            'chg': {},
            'extensions': [
                {
                    'command': 'idn',
                    'table':   'fr',
                    'name':    'testdomain.test',
                }
            ],
            'clTRID': 'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
