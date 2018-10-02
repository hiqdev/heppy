#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainUpdate(TestCase):

    def test_render_domain_update_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:update>
        </update>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
        })

    def test_render_domain_update_add_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:add>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:add>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'add': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_update_rem_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:rem>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:rem>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'rem': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_update_chg_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:chg>
                    <domain:registrant>jd1234</domain:registrant>
                    <domain:authInfo>
                        <domain:pw>2fooBAR</domain:pw>
                    </domain:authInfo>
                </domain:chg>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'chg': {
                'registrant':   'jd1234',
                'pw':           '2fooBAR'
            },
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_update_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:add>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:add>
                <domain:rem>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:rem>
                <domain:chg>
                    <domain:registrant>jd1234</domain:registrant>
                    <domain:authInfo>
                        <domain:pw>2fooBAR</domain:pw>
                    </domain:authInfo>
                </domain:chg>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'add': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'rem': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'chg': {
                'registrant':   'jd1234',
                'pw':           '2fooBAR'
            },
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
