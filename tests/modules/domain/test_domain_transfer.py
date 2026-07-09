#!/usr/bin/env python3

import unittest
from ..TestCase import TestCase


class TestDomainTransfer(TestCase):

    def test_render_domain_transfer_op_query_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'testdomain.test',
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_transfer_op_query_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:authInfo>
                    <domain:pw roid="TST0002-REP">tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'testdomain.test',
            'pw':       'tR4!xPass',
            'roid':     'TST0002-REP',
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_transfer_op_request_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'request',
            'name':     'testdomain.test',
            'clTRID':   'XXXX-11',
        })

    def test_render_domain_transfer_op_request_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:period unit="y">1</domain:period>
                <domain:authInfo>
                    <domain:pw roid="TST0002-REP">tR4!xPass</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'request',
            'name':     'testdomain.test',
            'period':   1,
            'pw':       'tR4!xPass',
            'roid':     'TST0002-REP',
            'clTRID':   'XXXX-11',
        })

    def test_parse_domain_tranfer_op_query_response(self):
        self.assertResponse({
            'acDate':       '2000-06-11T22:00:00.0Z',
            'acID':         'ClientY',
            'clTRID':       'ABC-12345',
            'exDate':       '2002-09-08T22:00:00.0Z',
            'name':         'testdomain.test',
            'reDate':       '2000-06-06T22:00:00.0Z',
            'reID':         'ClientX',
            'result_code':  '1000',
            'result_msg':   'Command completed successfully',
            'svTRID':       '54322-XYZ',
            'trStatus':     'pending'
        }, '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1000">
            <msg>Command completed successfully</msg>
        </result>
        <resData>
                <domain:trnData
             xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:trStatus>pending</domain:trStatus>
                <domain:reID>ClientX</domain:reID>
                <domain:reDate>2000-06-06T22:00:00.0Z</domain:reDate>
                <domain:acID>ClientY</domain:acID>
                <domain:acDate>2000-06-11T22:00:00.0Z</domain:acDate>
                <domain:exDate>2002-09-08T22:00:00.0Z</domain:exDate>
            </domain:trnData>
        </resData>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54322-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')

    def test_parse_domain_tranfer_op_request_response(self):
        self.assertResponse({
            'acDate':       '2000-06-13T22:00:00.0Z',
            'acID':         'ClientY',
            'clTRID':       'ABC-12345',
            'exDate':       '2002-09-08T22:00:00.0Z',
            'name':         'testdomain.test',
            'reDate':       '2000-06-08T22:00:00.0Z',
            'reID':         'ClientX',
            'result_code':  '1001',
            'result_msg':   'Command completed successfully; action pending',
            'svTRID':       '54322-XYZ',
            'trStatus':     'pending'
        }, '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1001">
            <msg>Command completed successfully; action pending</msg>
        </result>
        <resData>
            <domain:trnData
             xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>testdomain.test</domain:name>
                <domain:trStatus>pending</domain:trStatus>
                <domain:reID>ClientX</domain:reID>
                <domain:reDate>2000-06-08T22:00:00.0Z</domain:reDate>
                <domain:acID>ClientY</domain:acID>
                <domain:acDate>2000-06-13T22:00:00.0Z</domain:acDate>
                <domain:exDate>2002-09-08T22:00:00.0Z</domain:exDate>
            </domain:trnData>
        </resData>
        <trID>
            <clTRID>ABC-12345</clTRID>
            <svTRID>54322-XYZ</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main(verbosity=2)
