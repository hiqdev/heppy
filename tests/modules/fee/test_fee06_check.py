# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFee06Check(TestCase):

    def test_parse_fee06_check_response(self):
        # Structure and values confirmed against a real registry (Google's
        # registry-sandbox OTE, fee-0.6): <fee:cd> wraps <fee:name>/<fee:currency>/
        # <fee:command>/<fee:period>/<fee:fee>, keyed by fee:name (fee.py's
        # default parse_cd_tag_extension key='name' is correct here — fee06
        # only needed the chkData -> descend -> parse_cd routing fix, not a
        # different key).
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
                    'currency':    'USD',
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
      <fee:chkData xmlns:fee="urn:ietf:params:xml:ns:fee-0.6">
        <fee:cd>
          <fee:name>domaincontext.domaincontext-ga</fee:name>
          <fee:currency>USD</fee:currency>
          <fee:command>create</fee:command>
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
