#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnCreate(TestCase):

    def test_render_idn_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>silverfire.me</domain:name>
                <domain:registrant>jd1234</domain:registrant>
                <domain:ns>
                    <domain:hostObj>ns1.example.net</domain:hostObj>
                    <domain:hostObj>ns2.example.net</domain:hostObj>
                </domain:ns>
                <domain:authInfo>
                    <domain:pw>2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <extension>
            <idn:create xmlns:idn="urn:afilias:params:xml:ns:idn-1.0">
                <idn:script>ua</idn:script>
            </idn:create>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':      'domain:create',
            'name':         'silverfire.me',
            'registrant':   'jd1234',
            'nss': [
                'ns1.example.net',
                'ns2.example.net'
            ],
            'pw':           '2fooBAR',
            'extensions': [
                {
                    'command': 'idn:create',
                    'script':   'ua'
                }
            ],
            'clTRID':       'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
