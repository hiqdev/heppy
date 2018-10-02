#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactCheck(TestCase):

    def test_render_contact_check_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <check>
            <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
                <contact:id>sah8013</contact:id>
                <contact:id>8013sah</contact:id>
            </contact:check>
        </check>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command': 'contact:check',
            'ids': [
                'sh8013',
                'sah8013',
                '8013sah'
            ],
            'clTRID': 'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
