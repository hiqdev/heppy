#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactInfo(TestCase):

    def test_render_contact_info_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'sh8013',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
                <contact:authInfo>
                    <contact:pw>2fooBAR</contact:pw>
                </contact:authInfo>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'sh8013',
            'pw':       '2fooBAR',
            'clTRID':   'XXXX-11',
        })

    def test_parse_contact_info_response(self):
        self.assertResponse({
            'cc':           'US',
            'city':         'Dulles',
            'clID':         'OTE1186-EP1',
            'clTRID':       'XXXX-11',
            'crDate':       '2018-10-04T12:09:03.0Z',
            'crID':         'OTE1186-EP1',
            'email':        'jdoe@example.com',
            'fax':          '+1.7035555556',
            'id':           'sh8013',
            'name':         'John Doe',
            'org':          'Example Inc.',
            'pc':           '20166-6503',
            'pw':           '2fooBAR',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'roid':         'C2775978-AGRS',
            'sp':           'VA',
            'statuses': {
                'ok': None
            },
            'street':       'Suite 100',
            'svTRID':       'SRO-1538656213350',
            'voice':        '+1.7035555555'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <contact:infData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                <contact:id>sh8013</contact:id>
                <contact:roid>C2775978-AGRS</contact:roid>
                <contact:status s="ok"/>
                <contact:postalInfo type="int">
                    <contact:name>John Doe</contact:name>
                    <contact:org>Example Inc.</contact:org>
                    <contact:addr>
                        <contact:street>123 Example Dr.</contact:street>
                        <contact:street>Suite 100</contact:street>
                        <contact:city>Dulles</contact:city>
                        <contact:sp>VA</contact:sp>
                        <contact:pc>20166-6503</contact:pc>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:voice>+1.7035555555</contact:voice>
                <contact:fax>+1.7035555556</contact:fax>
                <contact:email>jdoe@example.com</contact:email>
                <contact:clID>OTE1186-EP1</contact:clID>
                <contact:crID>OTE1186-EP1</contact:crID>
                <contact:crDate>2018-10-04T12:09:03.0Z</contact:crDate>
                <contact:authInfo>
                    <contact:pw>2fooBAR</contact:pw>
                </contact:authInfo>
            </contact:infData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538656213350</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
