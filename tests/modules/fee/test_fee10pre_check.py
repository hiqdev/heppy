# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee10PreCheck(TestCase):

    def test_parse_fee10pre_check_response(self):
        # draft-ietf-regext-epp-fees used the bare
        # urn:ietf:params:xml:ns:fee-1.0 namespace through revision -12,
        # before renaming it to urn:ietf:params:xml:ns:epp:fee-1.0 in -13
        # (what fee10/RFC 8748 use). Without a registered nsmap entry for the
        # pre-rename URI, Doc.get_module() returns None and Response.parse()
        # silently drops the whole extension block. Same wire format as
        # fee10 otherwise — this locks in that it now resolves and parses.
        self.assertResponse({
            'avails':      {'example.com': '1'},
            'clTRID':      'ABC-12345',
            'currency':    'USD',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'example.com': {
                    'objID':       'example.com',
                    'avail':       '1',
                    'command':     'create',
                    'period':      '2',
                    'unit':        'y',
                    'fee':         '10.00',
                    'description': 'registration fee',
                    'refundable':  '1',
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
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-1.0">
        <fee:currency>USD</fee:currency>
        <fee:cd avail="1">
          <fee:objID>example.com</fee:objID>
          <fee:command name="create">
            <fee:period unit="y">2</fee:period>
            <fee:fee description="Registration Fee" refundable="1">10.00</fee:fee>
          </fee:command>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
