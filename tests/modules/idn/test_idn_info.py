#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnInfo(TestCase):

    def test_parse_idn_info_response(self):
        self.assertResponse({
            'clID':         'ClientA',
            'clTRID':       'CLI-1097604691520',
            'crDate':       '2004-10-12T17:57:41.0Z',
            'crID':         'ClientA',
            'exDate':       '2006-10-12T17:57:41.0Z',
            'name':         'xn--bq-uia.info',
            'nss': [
                'ns1.valid.info',
                'ns2.valid.info'
            ],
            'pw':           'tR4!xPass',
            'registrant':   'OTNE-C1',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'roid':         'D224-LRMS',
            'statuses': {
                'ok': 'ok'
            },
            'svTRID':       'SRO-1097604691524',
            'tech':         ['OTNE-C2'],
            'admin':        ['OTNE-C3'],
            'billing':      ['OTNE-C4'],
            'table':        'de',
            'extensions':   [],
        }, '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<epp xmlns='urn:ietf:params:xml:ns:epp-1.0'>
    <response>
        <result code='1000'>
            <msg lang='en-US'>Command completed successfully</msg>
        </result>
        <resData>
            <domain:infData xmlns:domain='urn:ietf:params:xml:ns:domain-1.0'>
                <domain:name>xn--bq-uia.info</domain:name>
                <domain:roid>D224-LRMS</domain:roid>
                <domain:status s='ok'/>
                <domain:registrant>OTNE-C1</domain:registrant>
                <domain:contact type='tech'>OTNE-C2</domain:contact>
                <domain:contact type='admin'>OTNE-C3</domain:contact>
                <domain:contact type='billing'>OTNE-C4</domain:contact>
                <domain:ns>
                    <domain:hostObj>ns1.valid.info</domain:hostObj>
                    <domain:hostObj>ns2.valid.info</domain:hostObj>
                </domain:ns>
                <domain:clID>ClientA</domain:clID>
                <domain:crID>ClientA</domain:crID>
                <domain:crDate>2004-10-12T17:57:41.0Z</domain:crDate>
                <domain:exDate>2006-10-12T17:57:41.0Z</domain:exDate>
                <domain:authInfo>
                    <domain:pw>tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:infData>
        </resData>
        <extension>
            <idn:infData xmlns:idn='urn:ietf:params:xml:ns:idn-1.0'>
                <idn:table>de</idn:table>
            </idn:infData>
        </extension>
        <trID>
            <clTRID>CLI-1097604691520</clTRID>
            <svTRID>SRO-1097604691524</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_ietf_idn_language_response(self):
        self.assertResponse({
            'result_code': '1000',
            'result_msg': 'Command completed successfully',
            'clTRID': 'aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb',
            'svTRID': 'cccccccc-3333-4444-5555-dddddddddddd',
            'name': 'xn--e1afmapc.xn--80akhbyknj4f',
            'roid': '10000000000001_DOMAIN-KEYSYS',
            'statuses': {
                'clientTransferProhibited': 'clientTransferProhibited',
                'clientDeleteProhibited': 'clientDeleteProhibited',
            },
            'registrant': 'P-TEST01',
            'admin': ['P-TEST01'],
            'tech': ['P-TEST01'],
            'billing': ['P-TEST01'],
            'nss': [
                'ns1.example.com',
                'ns2.example.com',
                'ns3.example.net',
                'ns4.example.net',
            ],
            'clID': 'testregistrar',
            'crID': 'testregistrar',
            'crDate': '2025-01-01T00:00:00.0Z',
            'upID': 'testregistrar',
            'upDate': '2025-06-01T00:00:00.0Z',
            'exDate': '2026-01-01T00:00:00.0Z',
            'pw': 'test-auth-pw',
            'extensions': [],
            'renDate': '2026-02-01T00:00:00.0Z',
            'punDate': '2026-01-01T00:00:00.0Z',
            'domain-roid': 'Dabcdef01-80ASEHDB',
            'idn-language': 'rus',
            'language': 'rus',
            'renewalmode': 'AUTOEXPIRE',
            'transferlock': '1',
            'transfermode': 'DEFAULT',
        }, '''<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <domain:infData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
        <domain:name>xn--e1afmapc.xn--80akhbyknj4f</domain:name>
        <domain:roid>10000000000001_DOMAIN-KEYSYS</domain:roid>
        <domain:status s="clientTransferProhibited"/>
        <domain:status s="clientDeleteProhibited"/>
        <domain:registrant>P-TEST01</domain:registrant>
        <domain:contact type="admin">P-TEST01</domain:contact>
        <domain:contact type="tech">P-TEST01</domain:contact>
        <domain:contact type="billing">P-TEST01</domain:contact>
        <domain:ns>
          <domain:hostObj>NS1.EXAMPLE.COM</domain:hostObj>
          <domain:hostObj>NS2.EXAMPLE.COM</domain:hostObj>
          <domain:hostObj>NS3.EXAMPLE.NET</domain:hostObj>
          <domain:hostObj>NS4.EXAMPLE.NET</domain:hostObj>
        </domain:ns>
        <domain:clID>testregistrar</domain:clID>
        <domain:crID>testregistrar</domain:crID>
        <domain:crDate>2025-01-01T00:00:00.0Z</domain:crDate>
        <domain:upID>testregistrar</domain:upID>
        <domain:upDate>2025-06-01T00:00:00.0Z</domain:upDate>
        <domain:exDate>2026-01-01T00:00:00.0Z</domain:exDate>
        <domain:authInfo>
          <domain:pw>test-auth-pw</domain:pw>
        </domain:authInfo>
      </domain:infData>
    </resData>
    <extension>
      <keysys:resData xmlns:keysys="http://www.key-systems.net/epp/keysys-1.0">
        <keysys:infData>
          <keysys:renDate>2026-02-01T00:00:00.0Z</keysys:renDate>
          <keysys:punDate>2026-01-01T00:00:00.0Z</keysys:punDate>
          <keysys:domain-roid>Dabcdef01-80ASEHDB</keysys:domain-roid>
          <keysys:idn-language>rus</keysys:idn-language>
          <keysys:renewalmode>AUTOEXPIRE</keysys:renewalmode>
          <keysys:transferlock>1</keysys:transferlock>
          <keysys:transfermode>DEFAULT</keysys:transfermode>
        </keysys:infData>
      </keysys:resData>
      <idn:language xmlns:idn="urn:ietf:params:xml:ns:idn-1.0">rus</idn:language>
    </extension>
    <trID>
      <clTRID>aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb</clTRID>
      <svTRID>cccccccc-3333-4444-5555-dddddddddddd</svTRID>
    </trID>
  </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
