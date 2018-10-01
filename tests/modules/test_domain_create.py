#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestDomainCreate(TestCase):

    def test_request_create_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:create',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_request_create(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:period unit="y">2</domain:period>
                <domain:registrant>jd1234</domain:registrant>
                <domain:ns>
                    <domain:hostObj>ns1.example.net</domain:hostObj>
                    <domain:hostObj>ns2.example.net</domain:hostObj>
                </domain:ns>
                <domain:contact type="admin">sh8013</domain:contact>
                <domain:contact type="tech">sh8014</domain:contact>
                <domain:contact type="billing">sh8015</domain:contact>
                <domain:authInfo>
                    <domain:pw>2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':      'domain:create',
            'name':         'example.com',
            'period':       2,
            'registrant':   'jd1234',
            'nss': [
                'ns1.example.net',
                'ns2.example.net'
            ],
            'admin':        'sh8013',
            'tech':         'sh8014',
            'billing':      'sh8015',
            'pw':           '2fooBAR',
            'clTRID':       'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
