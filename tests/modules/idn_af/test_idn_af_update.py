# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestIdnAfUpdate(TestCase):

    def test_render_idn_af_update_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>xn--bq-uia.info</domain:name>
                <domain:chg/>
            </domain:update>
        </update>
        <extension>
            <idn:update xmlns:idn="urn:afilias:params:xml:ns:idn-1.0">
                <idn:chg>
                    <idn:script>Latn</idn:script>
                </idn:chg>
            </idn:update>
        </extension>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>
''', {
            'command':  'domain:update',
            'name':     'xn--bq-uia.info',
            'chg': {},
            'extensions': [
                {
                    'command':  'idn_af:update',
                    'script':   'Latn',
                }
            ],
            'clTRID': 'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main(verbosity=2)
