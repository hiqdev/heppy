#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnLangDefault(TestCase):

    def test_render_idnLang_default_request(self):
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
            <idnLang:tag xmlns:idnLang="http://www.verisign.com/epp/idnLang-1.0">ENG</idnLang:tag>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:create',
            'name':     'silverfire.me',
            'extensions': [
                {
                    'command':  'idnLang',
                    'language': 'ENG'
                }
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
