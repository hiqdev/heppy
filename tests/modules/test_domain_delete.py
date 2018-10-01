#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestDomainDelete(TestCase):

    def test_render_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:delete',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
