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
                'ok': None
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
            'clTRID': 'c49e1914-3beb-11f1-a663-525400634cb8',
            'svTRID': '3019f721-c790-4a4c-9b25-fb81e2f2ea37',
            'name': 'xn--90a0bg.xn--80asehdb',
            'roid': '22549399811484_DOMAIN-KEYSYS',
            'statuses': {
                'clientTransferProhibited': None,
                'clientDeleteProhibited': None,
            },
            'registrant': 'P-VFP2032',
            'admin': ['P-VFP2032'],
            'tech': ['P-VFP2032'],
            'billing': ['P-VFP2032'],
            'nss': [
                'ns1.spaceweb.ru',
                'ns2.spaceweb.ru',
                'ns3.spaceweb.pro',
                'ns4.spaceweb.pro',
            ],
            'clID': 'domaincontext',
            'crID': 'domaincontext',
            'crDate': '2025-03-05T11:42:37.0Z',
            'upID': 'domaincontext',
            'upDate': '2026-03-01T09:17:27.0Z',
            'exDate': '2027-03-05T11:42:37.0Z',
            'pw': 'qu!l3OX@cX',
            'extensions': [],
            'renDate': '2027-04-09T11:42:37.0Z',
            'punDate': '2027-03-05T11:42:37.0Z',
            'domain-roid': 'Dtsff16041-80ASEHDB',
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
        <domain:name>xn--90a0bg.xn--80asehdb</domain:name>
        <domain:roid>22549399811484_DOMAIN-KEYSYS</domain:roid>
        <domain:status s="clientTransferProhibited"/>
        <domain:status s="clientDeleteProhibited"/>
        <domain:registrant>P-VFP2032</domain:registrant>
        <domain:contact type="admin">P-VFP2032</domain:contact>
        <domain:contact type="tech">P-VFP2032</domain:contact>
        <domain:contact type="billing">P-VFP2032</domain:contact>
        <domain:ns>
          <domain:hostObj>NS1.SPACEWEB.RU</domain:hostObj>
          <domain:hostObj>NS2.SPACEWEB.RU</domain:hostObj>
          <domain:hostObj>NS3.SPACEWEB.PRO</domain:hostObj>
          <domain:hostObj>NS4.SPACEWEB.PRO</domain:hostObj>
        </domain:ns>
        <domain:clID>domaincontext</domain:clID>
        <domain:crID>domaincontext</domain:crID>
        <domain:crDate>2025-03-05T11:42:37.0Z</domain:crDate>
        <domain:upID>domaincontext</domain:upID>
        <domain:upDate>2026-03-01T09:17:27.0Z</domain:upDate>
        <domain:exDate>2027-03-05T11:42:37.0Z</domain:exDate>
        <domain:authInfo>
          <domain:pw>qu!l3OX@cX</domain:pw>
        </domain:authInfo>
      </domain:infData>
    </resData>
    <extension>
      <keysys:resData xmlns:keysys="http://www.key-systems.net/epp/keysys-1.0">
        <keysys:infData>
          <keysys:renDate>2027-04-09T11:42:37.0Z</keysys:renDate>
          <keysys:punDate>2027-03-05T11:42:37.0Z</keysys:punDate>
          <keysys:domain-roid>Dtsff16041-80ASEHDB</keysys:domain-roid>
          <keysys:idn-language>rus</keysys:idn-language>
          <keysys:renewalmode>AUTOEXPIRE</keysys:renewalmode>
          <keysys:transferlock>1</keysys:transferlock>
          <keysys:transfermode>DEFAULT</keysys:transfermode>
        </keysys:infData>
      </keysys:resData>
      <idn:language xmlns:idn="urn:ietf:params:xml:ns:idn-1.0">rus</idn:language>
    </extension>
    <trID>
      <clTRID>c49e1914-3beb-11f1-a663-525400634cb8</clTRID>
      <svTRID>3019f721-c790-4a4c-9b25-fb81e2f2ea37</svTRID>
    </trID>
  </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
