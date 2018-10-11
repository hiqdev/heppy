#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeTransfer(TestCase):

    def test_parse_fee_transfer_response(self):
        self.assertResponse({
            'acDate':       '2000-06-13T22:00:00.0Z',
            'acID':         'ClientY',
            'clTRID':       'ABC-12345',
            'exDate':       '2002-09-08T22:00:00.0Z',
            'name':         'example.com',
            'reDate':       '2000-06-08T22:00:00.0Z',
            'reID':         'ClientX',
            'result_code':  '1001',
            'result_msg':   'Command completed successfully; action pending',
            'svTRID':       '54322-XYZ',
            'trStatus':     'pending',
            'extensions': [
                {
                    'command':  'fee:transfer',
                    'currency': 'USD',
                    'fee':      '5.00'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1001">
            <msg>Command completed successfully; action pending</msg>
        </result>
        <resData>
            <domain:trnData
                xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:trStatus>pending</domain:trStatus>
                <domain:reID>ClientX</domain:reID>
                <domain:reDate>2000-06-08T22:00:00.0Z</domain:reDate>
                <domain:acID>ClientY</domain:acID>
                <domain:acDate>2000-06-13T22:00:00.0Z</domain:acDate>
                <domain:exDate>2002-09-08T22:00:00.0Z</domain:exDate>
            </domain:trnData>
        </resData>
        <extension>
            <fee:trnData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:trnData>
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
