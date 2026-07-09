#!/usr/bin/env python3

import unittest
from ..TestCase import TestCase


class TestFee11Check(TestCase):

    def test_parse_fee11_check_response_keyed_by_domain(self):
        # Regression: <fee:command name="create"> must NOT overwrite data['name']
        # that was captured from <fee:object><domain:name>. The result must be
        # keyed by the domain name, not by the command action string.
        self.assertResponse({
            'avails':      {'example.google': '1'},
            'clTRID':      'ABC-12345',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'example.google': {
                    'name':     'example.google',
                    'command':  'create',
                    'period':   '1',
                    'unit':     'y',
                    'currency': 'USD',
                    'fee':      '10.00',
                    'avail':    '1',
                }
            },
        }, '''<?xml version="1.0" encoding="utf-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000"><msg>Command completed successfully</msg></result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="1">example.google</domain:name>
        </domain:cd>
      </domain:chkData>
    </resData>
    <extension>
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.11">
        <fee:cd avail="1">
          <fee:object>
            <domain:name xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">example.google</domain:name>
          </fee:object>
          <fee:command name="create">
            <fee:period unit="y">1</fee:period>
          </fee:command>
          <fee:currency>USD</fee:currency>
          <fee:fee>10.00</fee:fee>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
