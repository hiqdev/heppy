#!/usr/bin/env python

import unittest
from ..TestCase import TestCase


class TestContactDelete(TestCase):

    def test_render_contact_delete_request(self):
        self.assertRequest('''<?xml version="1.0" ?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
        <delete>
            <contact:delete xmlns:contact="urn:ietf:params:xml:ns:contact-1.0">
                <contact:id>sh8013</contact:id>
            </contact:delete>
        </delete>
        <clTRID>XXXX-11</clTRID>
    </command>
</epp>''', {
            'command':  'contact:delete',
            'id':       'sh8013',
            'clTRID':   'XXXX-11',
        })


if __name__ == '__main__':
    unittest.main()
