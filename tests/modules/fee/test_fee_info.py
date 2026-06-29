#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeInfo(TestCase):

    def test_render_fee_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name hosts="all">testfree.test</domain:name>
            </domain:info>
        </info>
        <extension>
            <fee:info xmlns:fee="urn:ietf:params:xml:ns:fee-0.7">
                <fee:currency>USD</fee:currency>
                <fee:command phase="sunrise">create</fee:command>
                <fee:period unit="y">1</fee:period>
            </fee:info>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command': 'domain:info',
            'name': 'testfree.test',
            'extensions': [
                {
                    'command':  'fee:info',
                    'action':   'create',
                    'currency': 'USD',
                    'phase':    'sunrise',
                    'period':   1
                },
            ],
            'clTRID': 'XXXX-11',
        })

    def test_parse_fee_info_response(self):
        self.assertResponse({
            'admin':        ['tst0001'],
            'clID':         'ClientX',
            'clTRID':       'ABC-12345',
            'crDate':       '1999-04-03T22:00:00.0Z',
            'crID':         'ClientY',
            'exDate':       '2005-04-03T22:00:00.0Z',
            'hosts': [
                'ns1.testdomain.test',
                'ns2.testdomain.test'
            ],
            'name':     'testdomain.test',
            'nss': [
                'ns1.testdomain.test',
                'ns1.testns.test'
            ],
            'pw':           'tR4!xPass',
            'registrant':   'tst0002',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'roid':         'EXAMPLE1-REP',
            'statuses': {
                'ok': 'ok'
            },
            'svTRID':       '54322-XYZ',
            'tech':         ['tst0001'],
            'trDate':       '2000-04-08T09:00:00.0Z',
            'upDate':       '1999-12-03T09:00:00.0Z',
            'upID':         'ClientX',
            'extensions': [
                {
                    'action': 'create',
                    'command': 'fee:info',
                    'currency': 'USD',
                    'fee': '10.00',
                    'period': '1',
                    'phase': 'sunrise',
                    'unit': 'y'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <resData>
            <domain:infData
                xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:roid>EXAMPLE1-REP</domain:roid>
                <domain:status s="ok" />
                <domain:registrant>tst0002</domain:registrant>
                <domain:contact type="admin">tst0001</domain:contact>
                <domain:contact type="tech">tst0001</domain:contact>
                <domain:ns>
                    <domain:hostObj>ns1.testdomain.test</domain:hostObj>
                    <domain:hostObj>ns1.testns.test</domain:hostObj>
                </domain:ns>
                <domain:host>ns1.testdomain.test</domain:host>
                <domain:host>ns2.testdomain.test</domain:host>
                <domain:clID>ClientX</domain:clID>
                <domain:crID>ClientY</domain:crID>
                <domain:crDate>1999-04-03T22:00:00.0Z</domain:crDate>
                <domain:upID>ClientX</domain:upID>
                <domain:upDate>1999-12-03T09:00:00.0Z</domain:upDate>
                <domain:exDate>2005-04-03T22:00:00.0Z</domain:exDate>
                <domain:trDate>2000-04-08T09:00:00.0Z</domain:trDate>
                <domain:authInfo>
                    <domain:pw>tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:infData>
        </resData>
        <extension>
            <fee:infData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:action phase="sunrise">create</fee:action>
                <fee:period unit="y">1</fee:period>
                <fee:fee>10.00</fee:fee>
            </fee:infData>
        </extension>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54322-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
