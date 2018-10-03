#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostCreate(TestCase):

    def test_render_host_create_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <host:create xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:create',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })

    def test_render_host_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <host:create xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:addr ip="v4">192.0.2.2</host:addr>
                <host:addr ip="v4">192.0.2.29</host:addr>
                <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
            </host:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:create',
            'name':     'ns1.example1.com',
            'ips': [
                '192.0.2.2',
                '192.0.2.29',
                '1080:0:0:0:8:800:200C:417A'
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
