# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFeeCreate(TestCase):

    def test_render_fee_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:period unit="y">2</domain:period>
                <domain:ns>
                    <domain:hostObj>ns1.testns.test</domain:hostObj>
                    <domain:hostObj>ns2.testns.test</domain:hostObj>
                </domain:ns>
                <domain:registrant>tst0002</domain:registrant>
                <domain:contact type="admin">tst0001</domain:contact>
                <domain:contact type="tech">sh8014</domain:contact>
                <domain:contact type="billing">sh8015</domain:contact>
                <domain:authInfo>
                    <domain:pw>tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <extension>
            <fee:create xmlns:fee="urn:ietf:params:xml:ns:fee-0.7">
                <fee:currency>USD</fee:currency>
                <fee:fee>42.42</fee:fee>
            </fee:create>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':      'domain:create',
            'name':         'testdomain.test',
            'period':       2,
            'registrant':   'tst0002',
            'nss': [
                'ns1.testns.test',
                'ns2.testns.test'
            ],
            'admin':        'tst0001',
            'tech':         'sh8014',
            'billing':      'sh8015',
            'pw':           'tR4!xPass',
            'extensions': [
                {
                    'command':  'fee:create',
                    'currency': 'USD',
                    'fee':      42.42
                },
            ],
            'clTRID':       'XXXX-11',
        })

    def test_parse_fee_create_response(self):
        self.assertResponse({
            'clTRID':       'ABC-12345',
            'crDate':       '1999-04-03T22:00:00.0Z',
            'exDate':       '2001-04-03T22:00:00.0Z',
            'name':         'testdomain.test',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54321-XYZ',
            'extensions': [
                {
                    'command':  'fee:create',
                    'currency': 'USD',
                    'fee':      '5.00'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <resData>
            <domain:creData
                xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:crDate>1999-04-03T22:00:00.0Z</domain:crDate>
                <domain:exDate>2001-04-03T22:00:00.0Z</domain:exDate>
            </domain:creData>
        </resData>
        <extension>
            <fee:creData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:creData>
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
