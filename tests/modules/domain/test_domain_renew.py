#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainRenew(TestCase):

    def test_render_domain_renew_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <renew>
            <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:curExpDate>2020-04-03</domain:curExpDate>
                <domain:period unit="y">5</domain:period>
            </domain:renew>
        </renew>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':      'domain:renew',
            'name':         'example.com',
            'curExpDate':   '2020-04-03',
            'period':       5,
            'clTRID':       'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
