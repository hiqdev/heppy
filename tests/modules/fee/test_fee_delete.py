#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestFeeDelete(TestCase):

    def test_parse_fee_delete_response(self):
        self.assertResponse({
            'clTRID':       'ABC-12345',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54321-XYZ',
            'extensions': [
                {
                    'command':  'fee:delete',
                    'credit':   '5.00',
                    'currency': 'USD'
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <extension>
            <fee:delData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:credit>5.00</fee:credit>
            </fee:delData>
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
