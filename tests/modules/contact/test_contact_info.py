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
                <contact:id>sh8013</contact:id>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'sh8013',
            'clTRID':   'XXXX-11',
        })

    def test_render_contact_info_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <info>
            <contact:info xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
                <contact:authInfo>
                    <contact:pw>2fooBAR</contact:pw>
                </contact:authInfo>
            </contact:info>
        </info>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:info',
            'id':       'sh8013',
            'pw':       '2fooBAR',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
