#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactCheck(TestCase):

    def test_render_contact_update_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'sh8013',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_update_request_add(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <contact:update xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
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
            'id':       'sh8013',
            'add': {
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
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
                <contact:id>sh8013</contact:id>
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
            'id':       'sh8013',
            'rem': {
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
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
                <contact:id>sh8013</contact:id>
                <contact:chg>
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
                    <contact:authInfo>
                        <contact:pw>2fooBAR</contact:pw>
                    </contact:authInfo>
                </contact:chg>
            </contact:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:update',
            'id':       'sh8013',
            'chg': {
                'name':     'John Doe',
                'org':      'Example Inc.',
                'city':     'Dulles',
                'street1':  '123 Example Dr.',
                'street2':  'Suite 100',
                'sp':       'VA',
                'pc':       '20166-6503',
                'cc':       'US',
                'voice':    '+1.7035555555',
                'fax':      '+1.7035555556',
                'email':    'jdoe@example.com',
                'pw':       '2fooBAR',
            },
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
