#!/usr/bin/env python

import unittest
from heppy.Request import Request
from TestCase import TestCase

class TestDomain(TestCase):

    def test_domain_check(self):
        self.assertRequest('''
<?xml version="1.0" ?>
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
            'names': {
                0: 'example1.com',
                1: 'example2.com',
            },
            'clTRID':   'XXXX-11',
        })

    def test_domain_info(self):
        request = Request.buildFromDict({
            'command':  'domain:info',
            'name':     'example.com',
            'pw':       '2fooBAR',
            'clTRID':   'XXXX-11',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name hosts="all">example.com</domain:name>
                <domain:authInfo>
                    <domain:pw>2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', Request.prettifyxml(str(request)).strip())

    def test_domain_create_min(self):
        request = Request.buildFromDict({
            'command':  'domain:create',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', Request.prettifyxml(str(request)).strip())

    def test_domain_create(self):
        request = Request.buildFromDict({
            'command':      'domain:create',
            'name':         'example.com',
            'period':       2,
            'registrant':   'jd1234',
            'nss': {
                0: 'ns1.example.net',
                1: 'ns2.example.net'
            },
            'admin':        'sh8013',
            'tech':         'sh8014',
            'billing':      'sh8015',
            'pw':           '2fooBAR',
            'clTRID':       'XXXX-11',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:period unit="y">2</domain:period>
                <domain:registrant>jd1234</domain:registrant>
                <domain:ns>
                    <domain:hostObj>ns1.example.net</domain:hostObj>
                    <domain:hostObj>ns2.example.net</domain:hostObj>
                </domain:ns>
                <domain:contact type="admin">sh8013</domain:contact>
                <domain:contact type="tech">sh8014</domain:contact>
                <domain:contact type="billing">sh8015</domain:contact>
                <domain:authInfo>
                    <domain:pw>2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', Request.prettifyxml(str(request)).strip())

    def test_domain_delete(self):
        request = Request.buildFromDict({
            'command':  'domain:delete',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', Request.prettifyxml(str(request)).strip())

    def test_domain_renew(self):
        request = Request.buildFromDict({
            'command':      'domain:renew',
            'name':         'example.com',
            'curExpDate':   '2020-04-03',
            'period':       5,
            'clTRID':       'XXXX-11',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
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
</epp>''', Request.prettifyxml(str(request)).strip())

    def test_domain_update(self):
        request = Request.buildFromDict({
            'command':  'domain:update',
            'name':     'example.com',
        })

        self.assertEqual(
'''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:update>
        </update>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', Request.prettifyxml(str(request)).strip())


if __name__ == '__main__':
    unittest.main()
