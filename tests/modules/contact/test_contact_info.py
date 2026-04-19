#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactInfo(TestCase):

    def test_render_contact_info_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'tst0001',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>tst0001</contact:id>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'tst0001',
            'pw':       'tR4!xPass',
            'clTRID':   'XXXX-11',
        })

    def test_parse_contact_info_response(self):
        self.assertResponse({
            'cc':           'US',
            'city':         'Testville',
            'clID':         'OTE1186-EP1',
            'clTRID':       'XXXX-11',
            'crDate':       '2018-10-04T12:09:03.0Z',
            'crID':         'OTE1186-EP1',
            'email':        'test@example.test',
            'fax':          '+1.5005550002',
            'id':           'tst0001',
            'int': {
                'name': 'Test User',
                'org': 'Test Corp',
                'addr': {
                    'street': 'Apt 200',
                    'street1': '1 Test Ave',
                    'street2': 'Apt 200',
                    'city': 'Testville',
                    'sp': 'VA',
                    'pc': '20166-6503',
                    'cc': 'US',
                },
            },
            'name':         'Test User',
            'org':          'Test Corp',
            'pc':           '20166-6503',
            'pw':           'tR4!xPass',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'roid':         'C2775978-AGRS',
            'sp':           'VA',
            'statuses': {
                'ok': None
            },
            'street':       'Apt 200',
            'street1':      '1 Test Ave',
            'street2':      'Apt 200',
            'svTRID':       'SRO-1538656213350',
            'voice':        '+1.5005550001'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <contact:infData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                <contact:id>tst0001</contact:id>
                <contact:roid>C2775978-AGRS</contact:roid>
                <contact:status s="ok"/>
                <contact:postalInfo type="int">
                    <contact:name>Test User</contact:name>
                    <contact:org>Test Corp</contact:org>
                    <contact:addr>
                        <contact:street>1 Test Ave</contact:street>
                        <contact:street>Apt 200</contact:street>
                        <contact:city>Testville</contact:city>
                        <contact:sp>VA</contact:sp>
                        <contact:pc>20166-6503</contact:pc>
                        <contact:cc>US</contact:cc>
                    </contact:addr>
                </contact:postalInfo>
                <contact:voice>+1.5005550001</contact:voice>
                <contact:fax>+1.5005550002</contact:fax>
                <contact:email>test@example.test</contact:email>
                <contact:clID>OTE1186-EP1</contact:clID>
                <contact:crID>OTE1186-EP1</contact:crID>
                <contact:crDate>2018-10-04T12:09:03.0Z</contact:crDate>
                <contact:authInfo>
                    <contact:pw>tR4!xPass</contact:pw>
                </contact:authInfo>
            </contact:infData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538656213350</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_keysys_contact_info_response(self):
        self.assertResponse({
            'result_code': '1000',
            'result_msg': 'Command completed successfully',
            'id': 'P-TST0001',
            'roid': '000000001_CONTACT-KEYSYS',
            'statuses': {
                'linked': None,
                'ok': None,
            },
            'loc': {
                'name': 'Test Fakename',
                'addr': {
                    'street': '54',
                    'street1': 'Fake Street',
                    'street2': '54',
                    'city': 'Testburg',
                    'sp': None,
                    'pc': '100001',
                    'cc': 'TJ',
                },
            },
            'name': 'Test Fakename',
            'street': '54',
            'street1': 'Fake Street',
            'street2': '54',
            'city': 'Testburg',
            'sp': None,
            'pc': '100001',
            'cc': 'TJ',
            'voice': '+992.500555001',
            'fax': None,
            'email': 'contact@example.test',
            'clID': 'domaincontext',
            'crID': 'domaincontext',
            'crDate': '2026-02-03T09:40:09.0Z',
            'upID': 'domaincontext',
            'upDate': '2026-02-03T09:40:40.0Z',
            'pw': 'Test!Pwd1234',
            'extensions': [],
            'validated': '1',
            'verification-requested': '0',
            'verified': '0',
            'clTRID': '46c50a34-3c13-11f1-b389-525400634cb8',
            'svTRID': 'cb08776d-2b1f-4e70-87d0-326e0c432ba6',
        }, '''<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <contact:infData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>P-TST0001</contact:id>
        <contact:roid>000000001_CONTACT-KEYSYS</contact:roid>
        <contact:status s="linked"/>
        <contact:status s="ok"/>
        <contact:postalInfo type="loc">
          <contact:name>Test Fakename</contact:name>
          <contact:addr>
            <contact:street>Fake Street</contact:street>
            <contact:street>54</contact:street>
            <contact:city>Testburg</contact:city>
            <contact:sp/>
            <contact:pc>100001</contact:pc>
            <contact:cc>TJ</contact:cc>
          </contact:addr>
        </contact:postalInfo>
        <contact:voice>+992.500555001</contact:voice>
        <contact:fax/>
        <contact:email>contact@example.test</contact:email>
        <contact:clID>domaincontext</contact:clID>
        <contact:crID>domaincontext</contact:crID>
        <contact:crDate>2026-02-03T09:40:09.0Z</contact:crDate>
        <contact:upID>domaincontext</contact:upID>
        <contact:upDate>2026-02-03T09:40:40.0Z</contact:upDate>
        <contact:authInfo>
          <contact:pw>Test!Pwd1234</contact:pw>
        </contact:authInfo>
      </contact:infData>
    </resData>
    <extension>
      <keysys:resData xmlns:keysys="http://www.key-systems.net/epp/keysys-1.0">
        <keysys:contactInfData>
          <keysys:validated>1</keysys:validated>
          <keysys:verification-requested>0</keysys:verification-requested>
          <keysys:verified>0</keysys:verified>
        </keysys:contactInfData>
      </keysys:resData>
    </extension>
    <trID>
      <clTRID>46c50a34-3c13-11f1-b389-525400634cb8</clTRID>
      <svTRID>cb08776d-2b1f-4e70-87d0-326e0c432ba6</svTRID>
    </trID>
    </response>
</epp>
        ''')

    def test_parse_keysys_contact_info_response_private_person(self):
        self.assertResponse({
            'result_code': '1000',
            'result_msg': 'Command completed successfully',
            'id': 'P-TST0002',
            'roid': '000000002_CONTACT-KEYSYS',
            'statuses': {
                'linked': None,
                'ok': None,
            },
            'int': {
                'name': 'Ivan Testenko',
                'org': 'Private person',
                'addr': {
                    'street': 'Test Blvd 10',
                    'city': 'Testopol',
                    'sp': None,
                    'pc': '100002',
                    'cc': 'RU',
                },
            },
            'name': 'Ivan Testenko',
            'org': 'Private person',
            'street': 'Test Blvd 10',
            'city': 'Testopol',
            'sp': None,
            'pc': '100002',
            'cc': 'RU',
            'voice': '+7.5005550003',
            'fax': None,
            'email': 'contact2@example.test',
            'clID': 'domaincontext',
            'crID': 'domaincontext',
            'crDate': '2025-02-20T19:50:19.0Z',
            'pw': 'hH8?hC6.kN1^hB9!',
            'extensions': [],
            'validated': '1',
            'verification-requested': '0',
            'verified': '0',
            'clTRID': '6d3a79f8-3c20-11f1-b26c-525400634cb8',
            'svTRID': 'ba557e3f-7ad8-4bd3-9868-da5043a4f142',
        }, '''<?xml version="1.0" encoding="UTF-8"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <response>
    <result code="1000">
      <msg>Command completed successfully</msg>
    </result>
    <resData>
      <contact:infData xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
        <contact:id>P-TST0002</contact:id>
        <contact:roid>000000002_CONTACT-KEYSYS</contact:roid>
        <contact:status s="linked"/>
        <contact:status s="ok"/>
        <contact:postalInfo type="int">
          <contact:name>Ivan Testenko</contact:name>
          <contact:org>Private person</contact:org>
          <contact:addr>
            <contact:street>Test Blvd 10</contact:street>
            <contact:city>Testopol</contact:city>
            <contact:sp/>
            <contact:pc>100002</contact:pc>
            <contact:cc>RU</contact:cc>
          </contact:addr>
        </contact:postalInfo>
        <contact:voice>+7.5005550003</contact:voice>
        <contact:fax/>
        <contact:email>contact2@example.test</contact:email>
        <contact:clID>domaincontext</contact:clID>
        <contact:crID>domaincontext</contact:crID>
        <contact:crDate>2025-02-20T19:50:19.0Z</contact:crDate>
        <contact:authInfo>
          <contact:pw>hH8?hC6.kN1^hB9!</contact:pw>
        </contact:authInfo>
      </contact:infData>
    </resData>
    <extension>
      <keysys:resData xmlns:keysys="http://www.key-systems.net/epp/keysys-1.0">
        <keysys:contactInfData>
          <keysys:validated>1</keysys:validated>
          <keysys:verification-requested>0</keysys:verification-requested>
          <keysys:verified>0</keysys:verified>
        </keysys:contactInfData>
      </keysys:resData>
    </extension>
    <trID>
      <clTRID>6d3a79f8-3c20-11f1-b26c-525400634cb8</clTRID>
      <svTRID>ba557e3f-7ad8-4bd3-9868-da5043a4f142</svTRID>
    </trID>
  </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
