# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from heppy.Client import Client


class TestClient(unittest.TestCase):
    def make_client(self):
        client = Client.__new__(Client)
        client.socket = mock.Mock()
        client.address = '/tmp/epp.sock'
        return client

    def test_read_disconnects_on_success(self):
        client = self.make_client()
        with mock.patch('heppy.Client.Net.read', return_value='<epp/>'):
            self.assertEqual('<epp/>', client.read())
        self.assertIsNone(client.socket)

    def test_read_disconnects_on_truncated_frame(self):
        client = self.make_client()
        with mock.patch('heppy.Client.Net.read', side_effect=ConnectionError('connection closed inside EPP frame')):
            with self.assertRaises(ConnectionError):
                client.read()
        self.assertIsNone(client.socket)


if __name__ == '__main__':
    unittest.main()
