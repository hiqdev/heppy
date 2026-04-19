#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnCreate(TestCase):

    def test_render_idn_data_request_for_create(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testfree.test</domain:name>
                <domain:registrant>tst0002</domain:registrant>
                <domain:ns>
                    <domain:hostObj>ns1.testns.test</domain:hostObj>
                    <domain:hostObj>ns2.testns.test</domain:hostObj>
                </domain:ns>
                <domain:authInfo>
                    <domain:pw>tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <extension>
            <idn:data xmlns:idn="urn:ietf:params:xml:ns:idn-1.0">
                <idn:table>ua</idn:table>
                <idn:table>testfree.test</idn:table>
            </idn:data>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':      'domain:create',
            'name':         'testfree.test',
            'registrant':   'tst0002',
            'nss': [
                'ns1.testns.test',
                'ns2.testns.test'
            ],
            'pw':           'tR4!xPass',
            'extensions': [
                {
                    'command': 'idn',
                    'table':   'ua',
                    'name':    'testfree.test',
                }
            ],
            'clTRID':       'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
