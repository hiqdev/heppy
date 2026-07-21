# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee09Check(TestCase):

    def test_parse_fee09_check_response(self):
        # Per draft-brown-epp-fees-07 (fee-0.9): <fee:cd> holds a flat
        # <fee:objID> plus sibling currency/command/period/fee — no nested
        # <fee:command> children yet (that arrives later, in fee-0.11/0.12).
        # fee09 already overrides parse_cd with key='objID' for this; only the
        # chkData -> descend routing (inherited from the fee.py base fix) was
        # needed to actually reach it.
        self.assertResponse({
            'avails':      {'example.com': '1'},
            'clTRID':      'ABC-12345',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'example.com': {
                    'objID':       'example.com',
                    'currency':    'USD',
                    'command':     'create',
                    'phase':       'sunrise',
                    'period':      '1',
                    'unit':        'y',
                    'fee':         '5.00',
                    'description': 'Application Fee',
                    'refundable':  '0',
                },
            },
        }, '''<?xml version="1.0" encoding="utf-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000"><msg>Command completed successfully</msg></result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="1">example.com</domain:name>
        </domain:cd>
      </domain:chkData>
    </resData>
    <extension>
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.9">
        <fee:cd>
          <fee:objID>example.com</fee:objID>
          <fee:currency>USD</fee:currency>
          <fee:command phase="sunrise">create</fee:command>
          <fee:period unit="y">1</fee:period>
          <fee:fee description="Application Fee" refundable="0">5.00</fee:fee>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
