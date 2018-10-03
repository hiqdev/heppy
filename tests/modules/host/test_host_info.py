#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostInfo(TestCase):

    def test_render_contact_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <host:info xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:info',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
