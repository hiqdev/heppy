#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestEppInfo(TestCase):

    def test_render_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <obj:info xmlns:obj="urn:ietf:params:xml:ns:obj">
                <obj:name>example1.com</obj:name>
                <obj:name>example2.com</obj:name>
            </obj:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:info',
            'names': [
                'example1.com',
                'example2.com'
            ],
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
