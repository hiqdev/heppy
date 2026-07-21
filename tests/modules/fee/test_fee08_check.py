# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee08Check(TestCase):

    def test_parse_fee08_check_response(self):
        # fee08 is a plain pass-through of fee.py's default parse_cd
        # (name-keyed) — this locks in that the chkData -> descend -> parse_cd
        # routing fix applies here too, and that fee-0.8 resolves to the fee08
        # class (not silently falling back to some other version).
        self.assertResponse({
            'avails':      {'example.test': '1'},
            'clTRID':      'ABC-12345',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'example.test': {
                    'name':     'example.test',
                    'currency': 'USD',
                    'command':  'create',
                    'period':   '1',
                    'unit':     'y',
                    'fee':      '10.00',
                },
            },
        }, '''<?xml version="1.0" encoding="utf-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000"><msg>Command completed successfully</msg></result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="1">example.test</domain:name>
        </domain:cd>
      </domain:chkData>
    </resData>
    <extension>
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.8">
        <fee:cd>
          <fee:name>example.test</fee:name>
          <fee:currency>USD</fee:currency>
          <fee:command>create</fee:command>
          <fee:period unit="y">1</fee:period>
          <fee:fee>10.00</fee:fee>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
