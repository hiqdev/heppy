#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostUpdate(TestCase):

    def test_render_host_update_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'host:update',
            'name': 'ns1.example1.com',
            'clTRID': 'XXXX-11',
        })

    def test_render_host_update_add_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:add>
                    <host:addr ip="v4">192.0.2.2</host:addr>
                    <host:addr ip="v4">192.0.2.29</host:addr>
                    <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
                    <host:status s="clientHold">Payment overdue.</host:status>
                    <host:status s="clientUpdateProhibited"/>
                </host:add>
            </host:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'host:update',
            'name': 'ns1.example1.com',
            'add': {
                'ips': [
                    '192.0.2.2',
                    '192.0.2.29',
                    '1080:0:0:0:8:800:200C:417A'
                ],
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
                }
            },
            'clTRID': 'XXXX-11',
        })

    def test_render_host_update_rem_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:rem>
                    <host:addr ip="v4">192.0.2.2</host:addr>
                    <host:addr ip="v4">192.0.2.29</host:addr>
                    <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
                    <host:status s="clientHold">Payment overdue.</host:status>
                    <host:status s="clientUpdateProhibited"/>
                </host:rem>
            </host:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'host:update',
            'name': 'ns1.example1.com',
            'rem': {
                'ips': [
                    '192.0.2.2',
                    '192.0.2.29',
                    '1080:0:0:0:8:800:200C:417A'
                ],
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
                }
            },
            'clTRID': 'XXXX-11',
        })

    def test_render_host_update_chg_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:chg>
                    <host:name>ns2.example1.com</host:name>
                </host:chg>
            </host:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'host:update',
            'name': 'ns1.example1.com',
            'chg': {
                'name': 'ns2.example1.com',
            },
            'clTRID': 'XXXX-11',
        })

    def test_render_host_update_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:add>
                    <host:addr ip="v4">192.0.2.2</host:addr>
                    <host:addr ip="v4">192.0.2.29</host:addr>
                    <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
                    <host:status s="clientHold">Payment overdue.</host:status>
                    <host:status s="clientUpdateProhibited"/>
                </host:add>
                <host:rem>
                    <host:addr ip="v4">192.0.2.2</host:addr>
                    <host:addr ip="v4">192.0.2.29</host:addr>
                    <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
                    <host:status s="clientHold">Payment overdue.</host:status>
                    <host:status s="clientUpdateProhibited"/>
                </host:rem>
                <host:chg>
                    <host:name>ns2.example1.com</host:name>
                </host:chg>
            </host:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'host:update',
            'name': 'ns1.example1.com',
            'add': {
                'ips': [
                    '192.0.2.2',
                    '192.0.2.29',
                    '1080:0:0:0:8:800:200C:417A'
                ],
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
                }
            },
            'rem': {
                'ips': [
                    '192.0.2.2',
                    '192.0.2.29',
                    '1080:0:0:0:8:800:200C:417A'
                ],
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': None
                }
            },
            'chg': {
                'name': 'ns2.example1.com',
            },
            'clTRID': 'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
