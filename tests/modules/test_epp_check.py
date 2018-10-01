#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestEppHello(TestCase):

    def test_render_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <obj:check xmlns:obj="urn:ietf:params:xml:ns:obj">
                <obj:name>example1.com</obj:name>
                <obj:name>example2.com</obj:name>
            </obj:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:check',
            'names': [
                'example1.com',
                'example2.com'
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
