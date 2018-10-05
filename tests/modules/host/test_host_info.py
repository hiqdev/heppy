#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestHostInfo(TestCase):

    def test_render_host_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <host:info xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                <host:name>ns1.example1.com</host:name>
            </host:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'host:info',
            'name':     'ns1.example1.com',
            'clTRID':   'XXXX-11',
        })

    def test_parse_host_info_response(self):
        self.assertResponse({
            'clID':         'OTE1186-EP1',
            'clTRID':       'XXXX-11',
            'crDate':       '2018-10-05T09:32:07.0Z',
            'crID':         'OTE1186-EP1',
            'ips': [
                '192.0.2.2',
                '192.0.2.29',
                '1080:0:0:0:8:800:200c:417a'
            ],
            'name':         'ns1.silverfire.me',
            'result_code':  '1000',
            'result_lang':  'en-US',
            'result_msg':   'Command completed successfully',
            'roid':         'H151302-AGRS',
            'statuses': {
                'ok': None
            },
            'svTRID': 'SRO-1538734456408'
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
    <response>
        <result code="1000">
            <msg lang="en-US">Command completed successfully</msg>
        </result>
        <resData>
            <host:infData xmlns:host="urn:ietf:params:xml:ns:host-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                <host:name>ns1.silverfire.me</host:name>
                <host:roid>H151302-AGRS</host:roid>
                <host:status s="ok"/>
                <host:addr ip="v4">192.0.2.2</host:addr>
                <host:addr ip="v4">192.0.2.29</host:addr>
                <host:addr ip="v6">1080:0:0:0:8:800:200c:417a</host:addr>
                <host:clID>OTE1186-EP1</host:clID>
                <host:crID>OTE1186-EP1</host:crID>
                <host:crDate>2018-10-05T09:32:07.0Z</host:crDate>
            </host:infData>
        </resData>
        <trID>
            <clTRID>XXXX-11</clTRID>
            <svTRID>SRO-1538734456408</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
