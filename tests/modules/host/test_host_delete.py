#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostDelete(TestCase):

    def test_render_host_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <host:delete xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:delete',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
