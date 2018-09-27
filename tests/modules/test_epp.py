#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestDomain(TestCase):
    def test_hello(self):
        self.assertRequest('''
<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <hello/>
</epp>''', {
            'command':  'epp:hello',
        })


if __name__ == '__main__':
    unittest.main()
