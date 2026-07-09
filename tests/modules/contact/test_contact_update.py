# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestContactCheck(TestCase):

    def test_render_contact_update_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'tst0001',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_update_request_add(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:add>
                    <contact:status s="clientHold">Payment overdue.</contact:status>
                    <contact:status s="clientUpdateProhibited"/>
                </contact:add>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'tst0001',
            'add': {
                'statuses': {
                    'clientHold':               'Payment overdue.',
                    'clientUpdateProhibited':   None
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_update_request_rem(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:rem>
                    <contact:status s="clientHold">Payment overdue.</contact:status>
                    <contact:status s="clientUpdateProhibited"/>
                </contact:rem>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'tst0001',
            'rem': {
                'statuses': {
                    'clientHold':               'Payment overdue.',
                    'clientUpdateProhibited':   None
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_update_request_chg(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:chg>
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
                </contact:chg>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'tst0001',
            'chg': {
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
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_update_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:add>
                    <contact:status s="clientHold">Payment overdue.</contact:status>
                    <contact:status s="clientUpdateProhibited"/>
                </contact:add>
                <contact:rem>
                    <contact:status s="clientHold">Payment overdue.</contact:status>
                    <contact:status s="clientUpdateProhibited"/>
                </contact:rem>
                <contact:chg>
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
                </contact:chg>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'contact:update',
            'id': 'tst0001',
            'add': {
                'statuses': {
                    'clientHold':               'Payment overdue.',
                    'clientUpdateProhibited':   None
                }
            },
            'rem': {
                'statuses': {
                    'clientHold':               'Payment overdue.',
                    'clientUpdateProhibited':   None
                }
            },
            'chg': {
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
            },
            'clTRID': 'XXXX-11',
        })

    def test_parse_contact_update_response_success(self):
        self.assertResponse({
            'clTRID':       'XXXX-11',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'svTRID':       'SRW-425500000011139056'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139056</svTRID>
        </trID>
    </response>
</epp>
        ''')


    def test_parse_contact_update_response_fail(self):
        self.assertResponse({
            'clTRID':           'XXXX-11',
            'result_code':      '2004',
            'result_lang':      'en-US',
            'result_msg':       'Parameter value range error',
            'result_reason':    '2004:Parameter value range error (contact-status: clientHold)',
            'svTRID':           'SRW-425500000011139080'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="2004">
            <msg lang="en-US">Parameter value range error</msg>
            <value xmlns:oxrs="urn:afilias:params:xml:ns:oxrs-1.1">
                <oxrs:xcp>2004:Parameter value range error (contact-status: clientHold)</oxrs:xcp>
            </value>
        </result>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRW-425500000011139080</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
