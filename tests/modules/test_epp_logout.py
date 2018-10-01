#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestEppLogout(TestCase):

    def test_request_logout(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <logout/>
        <clTRID>ClientX</clTRID>
    </command>
</epp>''', {
            'command':  'epp:logout',
            'clTRID':   'ClientX',
        })


if __name__ == '__main__':
    unittest.main()
