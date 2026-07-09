#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestContactCreate(TestCase):

    def test_render_contact_create_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:postalInfo type="int">
                    <contact:name>Test User</contact:name>
                    <contact:addr>
                        <contact:city>Testville</contact:city>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:email>test@example.test</contact:email>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
            </contact:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:create',
            'id':       'tst0001',
            'name':     'Test User',
            'city':     'Testville',
            'cc':       'US',
            'email':    'test@example.test',
            'pw':       'tR4!xPass',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:postalInfo type="int">
                    <contact:name>Test User</contact:name>
                    <contact:org>Test Corp</contact:org>
                    <contact:addr>
                        <contact:street>1 Test Ave</contact:street>
                        <contact:street>Apt 200</contact:street>
                        <contact:city>Testville</contact:city>
                        <contact:sp>VA</contact:sp>
                        <contact:pc>20166-6503</contact:pc>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:voice>+1.5005550001</contact:voice>
                <contact:fax>+1.5005550002</contact:fax>
                <contact:email>test@example.test</contact:email>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
            </contact:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:create',
            'id':       'tst0001',
            'name':     'Test User',
            'org':      'Test Corp',
            'city':     'Testville',
            'street1':  '1 Test Ave',
            'street2':  'Apt 200',
            'sp':       'VA',
            'pc':       '20166-6503',
            'cc':       'US',
            'voice':    '+1.5005550001',
            'fax':      '+1.5005550002',
            'email':    'test@example.test',
            'pw':       'tR4!xPass',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_create_request_with_disclose(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:postalInfo type="int">
                    <contact:name>Test User</contact:name>
                    <contact:addr>
                        <contact:city>Testville</contact:city>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:email>test@example.test</contact:email>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
                <contact:disclose flag="0">
                    <contact:name type="int"/>
                    <contact:name type="loc"/>
                    <contact:org type="int"/>
                    <contact:org type="loc"/>
                    <contact:addr type="int"/>
                    <contact:addr type="loc"/>
                    <contact:voice/>
                    <contact:fax/>
                    <contact:email/>
                </contact:disclose>
            </contact:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:create',
            'id':       'tst0001',
            'name':     'Test User',
            'city':     'Testville',
            'cc':       'US',
            'email':    'test@example.test',
            'pw':       'tR4!xPass',
            'disclose': '0',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_create_request_with_disclose_flag_1(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:postalInfo type="int">
                    <contact:name>Test User</contact:name>
                    <contact:addr>
                        <contact:city>Testville</contact:city>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:email>test@example.test</contact:email>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
                <contact:disclose flag="1">
                    <contact:name type="int"/>
                    <contact:name type="loc"/>
                    <contact:org type="int"/>
                    <contact:org type="loc"/>
                    <contact:addr type="int"/>
                    <contact:addr type="loc"/>
                    <contact:voice/>
                    <contact:fax/>
                    <contact:email/>
                </contact:disclose>
            </contact:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:create',
            'id':       'tst0001',
            'name':     'Test User',
            'city':     'Testville',
            'cc':       'US',
            'email':    'test@example.test',
            'pw':       'tR4!xPass',
            'disclose': '1',
            'clTRID':   'XXXX-11',
        })

    def test_parse_contact_create_response(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'crDate':       '2018-10-04T12:09:03.0Z',
            'id':           'tst0001',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011130408'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <contact:creData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                <contact:id>tst0001</contact:id>
                <contact:crDate>2018-10-04T12:09:03.0Z</contact:crDate>
            </contact:creData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011130408</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
