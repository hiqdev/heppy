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


if __name__ == '__main__':
    unittest.main()
