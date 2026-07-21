# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee10Check(TestCase):

    def test_parse_fee10_check_response(self):
        # Structure and values confirmed against a real registry (Google's
        # registry-sandbox OTE, epp:fee-1.0 == our "fee10"): <fee:cd> holds a
        # flat <fee:objID>/<fee:class>, and price fields (<fee:period>,
        # <fee:fee>) nested inside <fee:command name="...">, keyed by objID.
        self.assertResponse({
            'avails':      {'domaincontext.domaincontext-ga': 'true'},
            'clTRID':      'ABC-12345',
            'currency':    'USD',
            'extensions':  [],
            'result_code': '1000',
            'result_msg':  'Command completed successfully',
            'svTRID':      '54322-XYZ',
            'fee': {
                'domaincontext.domaincontext-ga': {
                    'objID':       'domaincontext.domaincontext-ga',
                    'class':       'standard',
                    'command':     'create',
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
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:epp:fee-1.0">
        <fee:currency>USD</fee:currency>
        <fee:cd>
          <fee:objID>domaincontext.domaincontext-ga</fee:objID>
          <fee:class>standard</fee:class>
          <fee:command name="create">
            <fee:period unit="y">1</fee:period>
            <fee:fee description="create">8.00</fee:fee>
          </fee:command>
        </fee:cd>
      </fee:chkData>
    </extension>
    <trID><clTRID>ABC-12345</clTRID><svTRID>54322-XYZ</svTRID></trID>
  </response>
</epp>''')


if __name__ == '__main__':
    unittest.main()
