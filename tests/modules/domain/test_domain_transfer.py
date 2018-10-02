#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainTransfer(TestCase):

    def test_render_transfer_op_query_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_render_transfer_op_query_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw roid="JD1234-REP">2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'example.com',
            'pw':       '2fooBAR',
            'roid':     'JD1234-REP',
            'clTRID':   'XXXX-11',
        })

    def test_render_transfer_op_request_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'request',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_render_transfer_op_request_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:period unit="y">1</domain:period>
                <domain:authInfo>
                    <domain:pw roid="JD1234-REP">2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'request',
            'name':     'example.com',
            'period':   1,
            'pw':       '2fooBAR',
            'roid':     'JD1234-REP',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
