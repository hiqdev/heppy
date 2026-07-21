# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee21Check(TestCase):

    def test_parse_fee21_check_response(self):
        # Regression: draft-ietf-regext-epp-fees (fee-0.21/0.23) identifies
        # the checked object with a plain-text <fee:objID> and nests price
        # fields inside <fee:command name="...">. fee.parse_cd
        # (parse_cd_tag_extension, key='name') neither finds objID under
        # 'name' nor descends into <command> — it would silently key the
        # result by the command name ('create') instead of the domain, and
        # drop period/fee entirely. fee21.parse_cd must handle this shape
        # itself.
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
                    'avail':       '1',
                    'command':     'create',
                    'period':      '2',
                    'unit':        'y',
                    'fee':         '10.00',
                    'description': 'Registration Fee',
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
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.21">
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
