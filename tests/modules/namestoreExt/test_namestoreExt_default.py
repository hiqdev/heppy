#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestNamestoreExtDefault(TestCase):

    def test_render_namestoreExt_default_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.me</domain:name>
                <domain:name>silverfire.me</domain:name>
            </domain:check>
        </check>
        <extension>
            <namestoreExt:namestoreExt xmlns:namestoreExt="http://www.verisign-grs.com/epp/namestoreExt-1.1">
                <namestoreExt:subProduct>dotCOM</namestoreExt:subProduct>
            </namestoreExt:namestoreExt>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'example.me',
                'silverfire.me',
            ],
            'extensions': [
                {
                    'command':      'namestoreExt',
                    'subProduct':   'dotCOM'
                }
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
