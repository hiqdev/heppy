#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestDomainCheck(TestCase):

    def test_request_check(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example1.com</domain:name>
                <domain:name>example2.com</domain:name>
            </domain:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'example1.com',
                'example2.com',
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
