# -*- coding: utf-8 -*-

import ssl
import socket
import unittest
from unittest import mock

from heppy.EPP import EPP, REPP
from heppy.Daemon import Daemon


def make_epp():
    epp = EPP.__new__(EPP)
    epp.config = {}
    epp.socket = mock.Mock()
    epp.ssl = mock.Mock()
    return epp


class TestEPP(unittest.TestCase):
    def test_disconnect_closes_tls_connection(self):
        epp = make_epp()
        tls = epp.ssl
        epp.disconnect()
        tls.close.assert_called_once()
        self.assertIsNone(epp.ssl)
        self.assertIsNone(epp.socket)
        self.assertFalse(epp.is_connected())

    def test_write_ssl_error_drops_connection(self):
        epp = make_epp()
        with mock.patch('heppy.Net.write', side_effect=ssl.SSLError('[SSL: BAD_LENGTH] bad length')):
            with self.assertRaises(ssl.SSLError):
                epp.write('<hello/>')
        self.assertFalse(epp.is_connected())

    def test_write_timeout_drops_connection(self):
        epp = make_epp()
        with mock.patch('heppy.Net.write', side_effect=socket.timeout('timed out')):
            with self.assertRaises(socket.timeout):
                epp.write('<hello/>')
        self.assertFalse(epp.is_connected())

    def test_read_timeout_drops_connection(self):
        epp = make_epp()
        with mock.patch('heppy.Net.read', side_effect=socket.timeout('timed out')):
            with self.assertRaises(socket.timeout):
                epp.read()
        self.assertFalse(epp.is_connected())

    def test_non_socket_error_keeps_connection(self):
        epp = make_epp()
        with mock.patch('heppy.Net.write', side_effect=ValueError('bad data')):
            with self.assertRaises(ValueError):
                epp.write('<hello/>')
        self.assertTrue(epp.is_connected())


class TestDaemonReconnect(unittest.TestCase):
    def make_daemon(self, connected):
        daemon = Daemon.__new__(Daemon)
        daemon.handler = mock.MagicMock()
        daemon.client = mock.Mock(spec=REPP)
        daemon.client.is_connected.return_value = connected
        daemon.client.request.return_value = '<epp/>'
        daemon.reconnect = mock.Mock()
        return daemon

    def test_request_reconnects_when_connection_lost(self):
        daemon = self.make_daemon(connected=False)
        daemon.request('<hello/>')
        daemon.reconnect.assert_called_once()

    def test_request_keeps_live_connection(self):
        daemon = self.make_daemon(connected=True)
        self.assertEqual('<epp/>', daemon.request('<hello/>'))
        daemon.reconnect.assert_not_called()


if __name__ == '__main__':
    unittest.main()
