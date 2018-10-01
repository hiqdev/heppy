#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestEppHello(TestCase):

    def test_render_hello_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <hello/>
</epp>''', {
            'command':  'epp:hello',
        })

    def test_parse_hello_response_min(self):
        self.assertResponse({
            'svID': 'Example EPP server epp.example.com',
            'svDate': '2000-06-08T22:00:00.0Z',
            'version': '1.0',
            'lang': 'en',
            'objURIs': ['urn:ietf:params:xml:ns:domain-1.0'],
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <greeting>
        <svID>Example EPP server epp.example.com</svID>
        <svDate>2000-06-08T22:00:00.0Z</svDate>
        <svcMenu>
            <version>1.0</version>
            <lang>en</lang>
            <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
        </svcMenu>
    </greeting>
</epp>
        ''')

    def test_parse_hello_response(self):
        self.assertResponse({
            'svID': 'VeriSign Com/Net EPP Registration Server',
            'svDate': '2018-10-01T14:05:11Z',
            'version': '1.0',
            'lang': 'en',
            'objURIs': [
                'urn:ietf:params:xml:ns:domain-1.0',
                'urn:ietf:params:xml:ns:contact-1.0',
                'urn:ietf:params:xml:ns:host-1.0',
                'http://www.verisign.com/epp/registry-1.0',
                'http://www.verisign.com/epp/lowbalance-poll-1.0',
                'http://www.verisign.com/epp/rgp-poll-1.0',
            ],
            'extURIs': [
                'urn:ietf:params:xml:ns:secDNS-1.1',
                'http://www.verisign.com/epp/whoisInf-1.0',
                'http://www.verisign.com/epp/idnLang-1.0',
                'urn:ietf:params:xml:ns:coa-1.0',
                'http://www.verisign-grs.com/epp/namestoreExt-1.1',
                'http://www.verisign.com/epp/sync-1.0',
                'http://www.verisign.com/epp/relatedDomain-1.0',
                'urn:ietf:params:xml:ns:verificationCode-1.0',
                'urn:ietf:params:xml:ns:launch-1.0',
                'urn:ietf:params:xml:ns:rgp-1.0',
                'urn:ietf:params:xml:ns:changePoll-1.0',
            ],
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <greeting>
        <svID>VeriSign Com/Net EPP Registration Server</svID>
        <svDate>2018-10-01T14:05:11Z</svDate>
        <svcMenu>
            <version>1.0</version>
            <lang>en</lang>
            <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
            <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
            <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
            <objURI>http://www.verisign.com/epp/registry-1.0</objURI>
            <objURI>http://www.verisign.com/epp/lowbalance-poll-1.0</objURI>
            <objURI>http://www.verisign.com/epp/rgp-poll-1.0</objURI>
            <svcExtension>
                <extURI>urn:ietf:params:xml:ns:secDNS-1.1</extURI>
                <extURI>http://www.verisign.com/epp/whoisInf-1.0</extURI>
                <extURI>http://www.verisign.com/epp/idnLang-1.0</extURI>
                <extURI>urn:ietf:params:xml:ns:coa-1.0</extURI>
                <extURI>http://www.verisign-grs.com/epp/namestoreExt-1.1</extURI>
                <extURI>http://www.verisign.com/epp/sync-1.0</extURI>
                <extURI>http://www.verisign.com/epp/relatedDomain-1.0</extURI>
                <extURI>urn:ietf:params:xml:ns:verificationCode-1.0</extURI>
                <extURI>urn:ietf:params:xml:ns:launch-1.0</extURI>
                <extURI>urn:ietf:params:xml:ns:rgp-1.0</extURI>
                <extURI>urn:ietf:params:xml:ns:changePoll-1.0</extURI>
            </svcExtension>
        </svcMenu>
        <dcp>
            <access>
                <all/>
            </access>
            <statement>
                <purpose>
                    <admin/>
                    <other/>
                    <prov/>
                </purpose>
                <recipient>
                    <ours/>
                    <public/>
                    <unrelated/>
                </recipient>
                <retention>
                    <indefinite/>
                </retention>
            </statement>
        </dcp>
    </greeting>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
