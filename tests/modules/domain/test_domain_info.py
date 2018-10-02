#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestDomainInfo(TestCase):

    def test_render_domain_info_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name hosts="all">example.com</domain:name>
            </domain:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:info',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
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
</epp>''', {
            'command':  'domain:info',
            'name':     'example.com',
            'pw':       '2fooBAR',
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_info_response(self):
        self.assertResponse({
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'clTRID':       'AA-00',
            'svTRID':       'SRO-1538136049528',
            'name':         'evonames.info',
            'roid':         'D31051196-LRMS',
            'statuses':     {
                'clientDeleteProhibited':   None,
                'clientTransferProhibited': None,
                'clientUpdateProhibited':   None,
            },
            'registrant':   'EEVN_1002321N',
            'admin':        'EEVN_1002321N',
            'billing':      'EEVN_1002321N',
            'tech':         'EEVN_1002321N',
            'nss':          ['ns1.evonames.com', 'ns2.evonames.com'],
            'hosts':        ['ns1.nonstopo.info.evonames.info', 'ns2.nonstopo.info.evonames.info', 'nrie.evonames.info'],
            'clID':         '5186-EP',
            'crID':         '5186-EP',
            'crDate':       '2010-01-06T16:22:03.0Z',
            'upID':         '5186-EP',
            'upDate':       '2018-08-23T15:35:16.0Z',
            'exDate':       '2019-01-06T16:22:03.0Z',
            'pw':           '******',
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <domain:infData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                <domain:name>evonames.info</domain:name>
                <domain:roid>D31051196-LRMS</domain:roid>
                <domain:status s="clientDeleteProhibited"/>
                <domain:status s="clientTransferProhibited"/>
                <domain:status s="clientUpdateProhibited"/>
                <domain:registrant>EEVN_1002321N</domain:registrant>
                <domain:contact type="admin">EEVN_1002321N</domain:contact>
                <domain:contact type="billing">EEVN_1002321N</domain:contact>
                <domain:contact type="tech">EEVN_1002321N</domain:contact>
                <domain:ns>
                    <domain:hostObj>ns1.evonames.com</domain:hostObj>
                    <domain:hostObj>ns2.evonames.com</domain:hostObj>
                </domain:ns>
                <domain:host>ns1.nonstopo.info.evonames.info</domain:host>
                <domain:host>ns2.nonstopo.info.evonames.info</domain:host>
                <domain:host>nrie.evonames.info</domain:host>
                <domain:clID>5186-EP</domain:clID>
                <domain:crID>5186-EP</domain:crID>
                <domain:crDate>2010-01-06T16:22:03.0Z</domain:crDate>
                <domain:upID>5186-EP</domain:upID>
                <domain:upDate>2018-08-23T15:35:16.0Z</domain:upDate>
                <domain:exDate>2019-01-06T16:22:03.0Z</domain:exDate>
                <domain:authInfo>
                    <domain:pw>******</domain:pw>
                </domain:authInfo>
            </domain:infData>
        </resData>
        <trID>
            <clTRID>AA-00</clTRID>
            <svTRID>SRO-1538136049528</svTRID>
        </trID>
    </response>
</epp>''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
