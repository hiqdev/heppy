#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestIdnInfo(TestCase):

    def test_parse_idn_idn_response(self):
        self.assertResponse({
            'admin':        'OTNE-C3',
            'billing':      'OTNE-C4',
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
            'pw':           'foo-BAR',
            'registrant':   'OTNE-C1',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'roid':         'D224-LRMS',
            'statuses': {
                'ok': None
            },
            'svTRID':       'SRO-1097604691524',
            'tech':         'OTNE-C2',
            'extensions': [
                {
                    'command':  'idn:info',
                    'language': 'de'
                }
            ],
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
                    <domain:pw>foo-BAR</domain:pw>
                </domain:authInfo>
            </domain:infData>
        </resData>
        <extension>
            <idn:infData xmlns:idn='urn:afilias:params:xml:ns:idn-1.0'>
                <idn:script>de</idn:script>
            </idn:infData>
        </extension>
        <trID>
            <clTRID>CLI-1097604691520</clTRID>
            <svTRID>SRO-1097604691524</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
