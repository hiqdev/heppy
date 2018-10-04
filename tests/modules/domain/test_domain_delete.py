#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainDelete(TestCase):

    def test_render_domain_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:delete',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_parse_domain_delete_response(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011130577'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011130577</svTRID>
        </trID>
    </response>
</epp>
        ''')

if __name__ == '__main__':
    unittest.main(verbosity=2)
