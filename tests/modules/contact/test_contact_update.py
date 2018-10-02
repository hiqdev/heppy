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
                    'clientUpdateProhibited': ''
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
                    'clientUpdateProhibited': ''
                }
            },
            'clTRID':   'XXXX-11',
        })

if __name__ == '__main__':
    unittest.main()
