#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnDefault(TestCase):

    def test_render_idn_default_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>silverfire.me</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:create>
        </create>
        <extension>
            <idn:language xmlns:idn="urn:afilias:params:xml:ns:idn-1.0">en</idn:language>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:create',
            'name':     'silverfire.me',
            'extensions': [
                {
                    'command':  'idn',
                    'language': 'en'
                }
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
