#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestEppLogout(TestCase):

    def test_request_logout(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <logout/>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:logout',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
