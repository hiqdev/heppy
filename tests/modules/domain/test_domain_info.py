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
            'extensions': [],
#            'result_lang':  'en-US',
#            'result_msg':   'Command completed successfully',
            'msg':          'Command completed successfully',
            'clTRID':       'AA-00',
            'svTRID':       'SRO-1538136049528',
            'name':         'evonames.info',
            'roid':         'D31051196-LRMS',
            'statuses':     {
                'clientDeleteProhibited':   None,
                'clientTransferProhibited': None,
                'clientUpdateProhibited':   None,
            },
            'secDNS':       [
                {
                    'digest': 'C465DCD098389C47B6868D768B900A6AD16166CB',
                    'digestAlg': '8',
                    'digestType': '1',
                    'keyTag': '14197',
                }, {
                    'digest': '594EC8B84DB151F25C857E4E9A21A37605C7961CE98C5E6997EE69F225915227',
                    'digestAlg': '8',
                    'digestType': '2',
                    'keyTag': '14197',
                    'keyData': {
                        'flags': '257',
                        'protocol': '3',
                        'alg': '1',
                        'pubKey': 'AQPJ////4Q==',
                    },
                }, {
                    'digest': '8F7B2DD4FD07E3DDD90E040336D879EF9993E98C',
                    'digestAlg': '8',
                    'digestType': '1',
                    'keyTag': '40369',
                }, {
                    'digest': 'E99D7F9F12C1AF141051E9F118BA61F3B3F5A0ED6832AB93E6B93D9AD19AFD41',
                    'digestAlg': '8',
                    'digestType': '2',
                    'keyTag': '40369',
                }
            ],
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
        <extension>
            <secDNS:infData xmlns:secDNS="urn:ietf:params:xml:ns:secDNS-1.1">
                <secDNS:dsData>
                    <secDNS:keyTag>14197</secDNS:keyTag>
                    <secDNS:alg>8</secDNS:alg>
                    <secDNS:digestType>1</secDNS:digestType>
                    <secDNS:digest>C465DCD098389C47B6868D768B900A6AD16166CB</secDNS:digest>
                </secDNS:dsData>
                <secDNS:dsData>
                    <secDNS:keyTag>14197</secDNS:keyTag>
                    <secDNS:alg>8</secDNS:alg>
                    <secDNS:digestType>2</secDNS:digestType>
                    <secDNS:digest>594EC8B84DB151F25C857E4E9A21A37605C7961CE98C5E6997EE69F225915227</secDNS:digest>
                    <secDNS:keyData>
                        <secDNS:flags>257</secDNS:flags>
                        <secDNS:protocol>3</secDNS:protocol>
                        <secDNS:alg>1</secDNS:alg>
                        <secDNS:pubKey>AQPJ////4Q==</secDNS:pubKey>
                    </secDNS:keyData>
                </secDNS:dsData>
                <secDNS:dsData>
                    <secDNS:keyTag>40369</secDNS:keyTag>
                    <secDNS:alg>8</secDNS:alg>
                    <secDNS:digestType>1</secDNS:digestType>
                    <secDNS:digest>8F7B2DD4FD07E3DDD90E040336D879EF9993E98C</secDNS:digest>
                </secDNS:dsData>
                <secDNS:dsData>
                    <secDNS:keyTag>40369</secDNS:keyTag>
                    <secDNS:alg>8</secDNS:alg>
                    <secDNS:digestType>2</secDNS:digestType>
                    <secDNS:digest>E99D7F9F12C1AF141051E9F118BA61F3B3F5A0ED6832AB93E6B93D9AD19AFD41</secDNS:digest>
                </secDNS:dsData>
            </secDNS:infData>
        </extension>
        <trID>
            <clTRID>AA-00</clTRID>
            <svTRID>SRO-1538136049528</svTRID>
        </trID>
    </response>
</epp>''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
