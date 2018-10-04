#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactCheck(TestCase):

    def test_render_contact_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
                <contact:id>sah8013</contact:id>
                <contact:id>8013sah</contact:id>
            </contact:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'contact:check',
            'ids': [
                'sh8013',
                'sah8013',
                '8013sah'
            ],
            'clTRID': 'XXXX-11',
        })

    def test_parse_contact_check_response(self):
        self.assertResponse({
            'avails': {
                '8013sah': '1',
                'sah8013': '1',
                'sh8013': '0'
            },
            'clTRID': 'XXXX-11',
            'result_code': '1000',
            'result_lang': 'en-US',
            'result_msg': 'Command completed successfully',
            'svTRID': 'SRO-1538655515906'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <contact:chkData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                <contact:cd>
                    <contact:id avail="0">sh8013</contact:id>
                </contact:cd>
                <contact:cd>
                    <contact:id avail="1">sah8013</contact:id>
                </contact:cd>
                <contact:cd>
                    <contact:id avail="1">8013sah</contact:id>
                </contact:cd>
            </contact:chkData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538655515906</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
