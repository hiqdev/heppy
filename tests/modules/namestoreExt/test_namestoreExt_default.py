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

    def test_parse_namestoreExt_nsExtErrData_response(self):
        self.assertResponse({
            'clTRID':       'ABC-12345',
            'result_code':  '2306',
            'result_msg':   'Parameter value policy error',
            'svTRID':       '54321-XYZ',
            'extensions': [
                {
                    'code':     '1',
                    'command':  'namestoreExt:nsExtErrData',
                    'msg':      'Invalid sub-product'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="2306">
            <msg>Parameter value policy error</msg>
        </result>
        <extension>
            <namestoreExt:nsExtErrData 
            xmlns:namestoreExt="http://www.verisign-grs.com/epp/namestoreExt-1.1">
                <namestoreExt:msg code="1">
                    Invalid sub-product
                </namestoreExt:msg>
            </namestoreExt:nsExtErrData>
        </extension>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54321-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
