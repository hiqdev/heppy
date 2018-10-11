#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeRenew(TestCase):

    def test_parse_fee_renew_response(self):
        self.assertResponse({
            'clTRID':       'ABC-12345',
            'exDate':       '2005-04-03T22:00:00.0Z',
            'name':         'example.com',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54322-XYZ',
            'extensions': [
                {
                    'command':  'fee:renew',
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
            <domain:renData
                xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:exDate>2005-04-03T22:00:00.0Z</domain:exDate>
            </domain:renData>
        </resData>
        <extension>
            <fee:renData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:renData>
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
