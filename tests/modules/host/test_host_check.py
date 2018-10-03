#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostCheck(TestCase):

    def test_render_contact_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <host:check xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
                <host:name>ns2.example2.com</host:name>
                <host:name>ns3.example2.com</host:name>
            </host:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:check',
            'names': [
                'ns1.example1.com',
                'ns2.example2.com',
                'ns3.example2.com',
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
