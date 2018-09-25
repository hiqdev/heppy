#!/usr/bin/env python

import unittest

from pprint import pprint

from heppy.Request import Request

class TestDomain(unittest.TestCase):
    def test_domain_info(self):
        request = Request.buildFromDict({
            'command':  'epp:hello',
            'clTRID':   'XXXX-11',
        })

        self.assertEqual('''
<?xml version='1.0' encoding='UTF-8'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><hello /></epp>
'''.strip(), str(request))


if __name__ == '__main__':
    unittest.main()
