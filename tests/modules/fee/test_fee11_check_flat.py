# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee11CheckFlat(TestCase):

    def test_parse_fee11_check_response_flat_command(self):
        # Regression: confirmed against a real registry (Google's
        # registry-sandbox OTE, fee-0.11) — <fee:command> is plain text with
        # no "name" attribute, and <fee:period>/<fee:fee> are siblings of it
        # inside <fee:cd>, not nested children. Before this fix, parse_cd's
        # "elif tagname == 'command'" branch only ever read child.attrib['name']
        # or descended into nested children, so this real shape silently
        # dropped the command value entirely (present in fee-0.12's response,
        # which nests period/fee under <fee:command name="...">  — see
        # test_fee12_check.py).
        self.assertResponse({
            'avails':      {'domaincontext.domaincontext-ga': 'true'},
            'clTRID':      'ABC-12345',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'domaincontext.domaincontext-ga': {
                    'name':        'domaincontext.domaincontext-ga',
                    'avail':       'true',
                    'command':     'create',
                    'currency':    'USD',
                    'period':      '1',
                    'unit':        'y',
                    'fee':         '8.00',
                    'description': 'create',
                },
            },
        }, '''<?xml version="1.0" encoding="utf-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000"><msg>Command completed successfully</msg></result>
    <resData>
      <domain:chkData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:cd>
          <domain:name avail="true">domaincontext.domaincontext-ga</domain:name>
        </domain:cd>
      </domain:chkData>
    </resData>
    <extension>
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.11">
        <fee:cd avail="true">
          <fee:object>
            <domain:name xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">domaincontext.domaincontext-ga</domain:name>
          </fee:object>
          <fee:command>create</fee:command>
          <fee:currency>USD</fee:currency>
          <fee:period unit="y">1</fee:period>
          <fee:fee description="create">8.00</fee:fee>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
