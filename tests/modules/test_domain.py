#!/usr/bin/env python

import unittest
from TestCase import TestCase


class TestDomain(TestCase):

    def test_request_check(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example1.com</domain:name>
                <domain:name>example2.com</domain:name>
            </domain:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:check',
            'names': [
                'example1.com',
                'example2.com',
            ],
            'clTRID':   'XXXX-11',
        })

    def test_request_info_min(self):
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

    def test_request_info(self):
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

    def test_request_transfer_query_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_request_transfer_query(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="query">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw roid="JD1234-REP">2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'query',
            'name':     'example.com',
            'pw':       '2fooBAR',
            'roid':     'JD1234-REP',
            'clTRID':   'XXXX-11',
        })

    def test_request_transfer_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
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
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_request_transfer_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <transfer op="request">
            <domain:transfer xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:period unit="y">1</domain:period>
                <domain:authInfo>
                    <domain:pw roid="JD1234-REP">2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:transfer>
        </transfer>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:transfer',
            'op':       'request',
            'name':     'example.com',
            'period':   1,
            'pw':       '2fooBAR',
            'roid':     'JD1234-REP',
            'clTRID':   'XXXX-11',
        })

    def test_request_create_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:authInfo>
                    <domain:pw/>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:create',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_request_create(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <create>
            <domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:period unit="y">2</domain:period>
                <domain:registrant>jd1234</domain:registrant>
                <domain:ns>
                    <domain:hostObj>ns1.example.net</domain:hostObj>
                    <domain:hostObj>ns2.example.net</domain:hostObj>
                </domain:ns>
                <domain:contact type="admin">sh8013</domain:contact>
                <domain:contact type="tech">sh8014</domain:contact>
                <domain:contact type="billing">sh8015</domain:contact>
                <domain:authInfo>
                    <domain:pw>2fooBAR</domain:pw>
                </domain:authInfo>
            </domain:create>
        </create>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':      'domain:create',
            'name':         'example.com',
            'period':       2,
            'registrant':   'jd1234',
            'nss': [
                'ns1.example.net',
                'ns2.example.net'
            ],
            'admin':        'sh8013',
            'tech':         'sh8014',
            'billing':      'sh8015',
            'pw':           '2fooBAR',
            'clTRID':       'XXXX-11',
        })

    def test_request_delete(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <domain:delete xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:delete',
            'name':     'example.com',
            'clTRID':   'XXXX-11',
        })

    def test_request_renew(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <renew>
            <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:curExpDate>2020-04-03</domain:curExpDate>
                <domain:period unit="y">5</domain:period>
            </domain:renew>
        </renew>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':      'domain:renew',
            'name':         'example.com',
            'curExpDate':   '2020-04-03',
            'period':       5,
            'clTRID':       'XXXX-11',
        })

    def test_request_update_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
            </domain:update>
        </update>
        <clTRID>AA-00</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
        })

    def test_request_update_add(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:add>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:add>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'add': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_request_update_rem(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:rem>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:rem>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'rem': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'clTRID':   'XXXX-11',
        })

    def test_request_update_chg(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:chg>
                    <domain:registrant>jd1234</domain:registrant>
                    <domain:authInfo>
                        <domain:pw>2fooBAR</domain:pw>
                    </domain:authInfo>
                </domain:chg>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'chg': {
                'registrant':   'jd1234',
                'pw':           '2fooBAR'
            },
            'clTRID':   'XXXX-11',
        })

    def test_request_update(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <update>
            <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>example.com</domain:name>
                <domain:add>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:add>
                <domain:rem>
                    <domain:ns>
                        <domain:hostObj>ns1.example.net</domain:hostObj>
                        <domain:hostObj>ns2.example.net</domain:hostObj>
                    </domain:ns>
                    <domain:contact type="admin">sh8013</domain:contact>
                    <domain:contact type="tech">sh8014</domain:contact>
                    <domain:contact type="billing">sh8015</domain:contact>
                    <domain:status s="clientHold">Payment overdue.</domain:status>
                    <domain:status s="clientUpdateProhibited"/>
                </domain:rem>
                <domain:chg>
                    <domain:registrant>jd1234</domain:registrant>
                    <domain:authInfo>
                        <domain:pw>2fooBAR</domain:pw>
                    </domain:authInfo>
                </domain:chg>
            </domain:update>
        </update>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'domain:update',
            'name':     'example.com',
            'add': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'rem': {
                'nss': [
                    'ns1.example.net',
                    'ns2.example.net'
                ],
                'admin':    'sh8013',
                'tech':     'sh8014',
                'billing':  'sh8015',
                'statuses': {
                    'clientHold': 'Payment overdue.',
                    'clientUpdateProhibited': ''
                }
            },
            'chg': {
                'registrant':   'jd1234',
                'pw':           '2fooBAR'
            },
            'clTRID':   'XXXX-11',
        })

    def test_parse_info(self):
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
