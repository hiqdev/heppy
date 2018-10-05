#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactDelete(TestCase):

    def test_render_contact_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <contact:delete xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
            </contact:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:delete',
            'id':       'sh8013',
            'clTRID':   'XXXX-11',
        })

    def test_parse_contact_delete_response_success(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011139133'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139133</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_contact_delete_response_fail(self):
        self.assertResponse({
            'clTRID':           'XXXX-11',
            'result_code':      '2305',
            'result_lang':      'en-US',
            'result_msg':       'Object association prohibits operation',
            'result_reason':    '2305:Object association prohibits operation (sh8015)',
            'svTRID':           'SRW-425500000011139106'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="2305">
            <msg lang="en-US">Object association prohibits operation</msg>
            <value xmlns:oxrs="urn:afilias:params:xml:ns:oxrs-1.1">
                <oxrs:xcp>2305:Object association prohibits operation (sh8015)</oxrs:xcp>
            </value>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139106</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
