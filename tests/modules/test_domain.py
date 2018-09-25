#!/usr/bin/env python

import unittest

from pprint import pprint

from heppy.Request import Request

class TestDomain(unittest.TestCase):
    def test_domain_info(self):
        request = Request.buildFromDict({
            'command':  'domain:info',
            'name':     'asd.com',
            'clTRID':   'XXXX-11',
        })

        self.assertEqual('''
<?xml version='1.0' encoding='UTF-8'?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><command><info><domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0"><domain:name hosts="all">asd.com</domain:name></domain:info></info><clTRID>XXXX-11</clTRID></command></epp>
'''.strip(), str(request))


if __name__ == '__main__':
    unittest.main()
