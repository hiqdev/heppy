# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestIdnAfCreate(TestCase):

    def test_render_idn_af_create_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>xn--bq-uia.info</domain:name>
                <domain:ns>
                    <domain:hostObj>ns1.testns.test</domain:hostObj>
                    <domain:hostObj>ns2.testns.test</domain:hostObj>
                </domain:ns>
                <domain:registrant>tst0001</domain:registrant>
                <domain:authInfo>
                    <domain:pw>tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <extension>
            <idn:create xmlns:idn="urn:afilias:params:xml:ns:idn-1.0">
                <idn:script>Cyrl</idn:script>
            </idn:create>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':      'domain:create',
            'name':         'xn--bq-uia.info',
            'registrant':   'tst0001',
            'nss': [
                'ns1.testns.test',
                'ns2.testns.test'
            ],
            'pw':           'tR4!xPass',
            'extensions': [
                {
                    'command':  'idn_af:create',
                    'script':   'Cyrl',
                }
            ],
            'clTRID':       'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
