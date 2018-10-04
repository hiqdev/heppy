#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainRenew(TestCase):

    def test_render_domain_renew_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <renew>
            <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:curExpDate>2020-04-03</domain:curExpDate>
                <domain:period unit="y">5</domain:period>
            </domain:renew>
        </renew>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':      'domain:renew',
            'name':         'example.com',
            'curExpDate':   '2020-04-03',
            'period':       5,
            'clTRID':       'XXXX-11',
        })

    def test_parse_domain_renew_response(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'exDate':       '2021-10-04T15:35:20.0Z',
            'name':         'silverfire.me',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011130901'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <domain:renData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                <domain:name>silverfire.me</domain:name>
                <domain:exDate>2021-10-04T15:35:20.0Z</domain:exDate>
            </domain:renData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011130901</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
