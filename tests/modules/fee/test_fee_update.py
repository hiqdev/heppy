# -*- coding: utf-8 -*-

import unittest
from ..TestCase import TestCase


class TestFeeUpdate(TestCase):

    def test_render_fee_update_request(self):
        # legacy (fee-0.7-era) shape, via fee07 explicitly
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
            </domain:update>
        </update>
        <extension>
            <fee:update xmlns:fee="urn:ietf:params:xml:ns:fee-0.7">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:update>
        </extension>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'testdomain.test',
            'extensions': [
                {
                    'command':  'fee07:update',
                    'currency': 'USD',
                    'fee':      '5.00'
                },
            ],
            'clTRID':   'AA-00',
        })

    def test_render_fee_update_request_modern(self):
        # RFC 8748 (epp:fee-1.0) shape via the bare "fee" alias
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
            </domain:update>
        </update>
        <extension>
            <fee:update xmlns:fee="urn:ietf:params:xml:ns:epp:fee-1.0">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:update>
        </extension>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'testdomain.test',
            'extensions': [
                {
                    'command':  'fee:update',
                    'currency': 'USD',
                    'fee':      '5.00'
                },
            ],
            'clTRID':   'AA-00',
        })

    def test_render_domain_update_rgp_restore_with_fee(self):
        # the real-world case that motivated adding render_update: a premium
        # domain's rgp:restore (domain:update + rgp:restore op="request")
        # charges a fee, declared via a sibling fee:update extension on the
        # same domain:update command.
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
            </domain:update>
        </update>
        <extension>
            <rgp:update xmlns:rgp="urn:ietf:params:xml:ns:rgp-1.0">
                <rgp:restore op="request"/>
            </rgp:update>
            <fee:update xmlns:fee="urn:ietf:params:xml:ns:epp:fee-1.0">
                <fee:currency>USD</fee:currency>
                <fee:fee>75.00</fee:fee>
            </fee:update>
        </extension>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'testdomain.test',
            'extensions': [
                {'command': 'rgp:request'},
                {
                    'command':  'fee:update',
                    'currency': 'USD',
                    'fee':      '75.00'
                },
            ],
            'clTRID':   'AA-00',
        })

    def test_parse_fee_update_response(self):
        self.assertResponse({
            'clTRID':       'ABC-12345',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54321-XYZ',
            'extensions': [
                {
                    'command':  'fee:update',
                    'currency': 'USD',
                    'fee':      '5.00',
                }
            ],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <extension>
            <fee:updData xmlns:fee="urn:ietf:params:xml:ns:fee-0.5">
                <fee:currency>USD</fee:currency>
                <fee:fee>5.00</fee:fee>
            </fee:updData>
        </extension>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54321-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
