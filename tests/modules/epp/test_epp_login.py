#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestEppLogin(TestCase):

    def test_render_login_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <login>
            <clID>ClientX</clID>
            <pw>2fooBar</pw>
            <options>
                <version>1.0</version>
                <lang>en</lang>
            </options>
            <svcs>
                <objURI>urn:ietf:params:xml:ns:obj1</objURI>
                <objURI>urn:ietf:params:xml:ns:obj2</objURI>
                <objURI>urn:ietf:params:xml:ns:obj3</objURI>
            </svcs>
        </login>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'epp:login',
            'clID':     'ClientX',
            'pw':       '2fooBar',
            'objURIs': [
                'urn:ietf:params:xml:ns:obj1',
                'urn:ietf:params:xml:ns:obj2',
                'urn:ietf:params:xml:ns:obj3'
            ],
        })

    def test_render_login_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <login>
            <clID>ClientX</clID>
            <pw>2fooBar</pw>
            <newPW>bar-FOO2</newPW>
            <options>
                <version>4.2</version>
                <lang>ua</lang>
            </options>
            <svcs>
                <objURI>urn:ietf:params:xml:ns:obj1</objURI>
                <objURI>urn:ietf:params:xml:ns:obj2</objURI>
                <objURI>urn:ietf:params:xml:ns:obj3</objURI>
                <svcExtension>
                    <extURI>http://custom/obj1ext-1.0</extURI>
                    <extURI>http://custom/obj1ext-2.0</extURI>
                </svcExtension>
            </svcs>
        </login>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'epp:login',
            'clID':     'ClientX',
            'pw':       '2fooBar',
            'newPW':    'bar-FOO2',
            'version':  4.2,
            'lang':     'ua',
            'objURIs': [
                'urn:ietf:params:xml:ns:obj1',
                'urn:ietf:params:xml:ns:obj2',
                'urn:ietf:params:xml:ns:obj3'
            ],
            'extURIs': [
                'http://custom/obj1ext-1.0',
                'http://custom/obj1ext-2.0'
            ]
        })

    def test_render_login_request_alt(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <login>
            <clID>ClientX</clID>
            <pw>2fooBar</pw>
            <newPW>bar-FOO2</newPW>
            <options>
                <version>4.2</version>
                <lang>ua</lang>
            </options>
            <svcs>
                <objURI>urn:ietf:params:xml:ns:obj1</objURI>
                <objURI>urn:ietf:params:xml:ns:obj2</objURI>
                <objURI>urn:ietf:params:xml:ns:obj3</objURI>
                <svcExtension>
                    <extURI>http://custom/obj1ext-1.0</extURI>
                    <extURI>http://custom/obj1ext-2.0</extURI>
                </svcExtension>
            </svcs>
        </login>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':      'epp:login',
            'login':        'ClientX',
            'password':     '2fooBar',
            'newPassword':  'bar-FOO2',
            'version':      4.2,
            'lang':         'ua',
            'objURIs': [
                'urn:ietf:params:xml:ns:obj1',
                'urn:ietf:params:xml:ns:obj2',
                'urn:ietf:params:xml:ns:obj3'
            ],
            'extURIs': [
                'http://custom/obj1ext-1.0',
                'http://custom/obj1ext-2.0'
            ]
        })


if __name__ == '__main__':
    unittest.main()
