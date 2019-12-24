#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestEppPoll(TestCase):

    def test_render_epp_poll_request_min(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <poll op="req"/>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:poll',
            'clTRID':   'XXXX-11',
        })

    def test_render_epp_poll_op_req_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <poll op="req"/>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:poll',
            'op':       'req',
            'clTRID':   'XXXX-11',
        })

    def test_render_epp_poll_op_ack_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <poll msgID="42" op="ack"/>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'epp:poll',
            'op':       'ack',
            'msgID':    '42',
            'clTRID':   'XXXX-11',
        })

    def test_parse_epp_poll_response_transfer_rejected(self):
        self.assertResponse({
            'acDate':       '2019-12-24T09:57:17Z',
            'acID':         'godaddy',
            'qDate':        '2019-12-24T09:57:17Z',
            'clTRID':       'AA-00',
            'svTRID':       'RR-00',
            'name':         'EXAMPLE.COM',
            'reDate':       '2019-12-24T09:52:32Z',
            'reID':         '1418',
            'result_code':  '1301',
            'trStatus':     'clientRejected',
            'msg':          'Transfer Rejected.',
            'msgCount':     '1',
            'msgID':        '80076487',
        }, '''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <response>
        <result code="1301">
            <msg>Command completed successfully; ack to dequeue</msg>
        </result>
        <msgQ count="1" id="80076487">
            <qDate>2019-12-24T09:57:17Z</qDate>
            <msg>Transfer Rejected.</msg>
        </msgQ>
        <resData>
            <domain:trnData xmlns:domain="urn:ietf:params:xml:ns:domain-1.0">
                <domain:name>EXAMPLE.COM</domain:name>
                <domain:trStatus>clientRejected</domain:trStatus>
                <domain:reID>1418</domain:reID>
                <domain:reDate>2019-12-24T09:52:32Z</domain:reDate>
                <domain:acID>godaddy</domain:acID>
                <domain:acDate>2019-12-24T09:57:17Z</domain:acDate>
            </domain:trnData>
        </resData>
        <trID>
            <clTRID>AA-00</clTRID>
            <svTRID>RR-00</svTRID>
        </trID>
    </response>
</epp>
        ''')


if __name__ == '__main__':
    unittest.main()
