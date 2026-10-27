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

    def test_read_truncated_frame_drops_connection(self):
        epp = make_epp()
        with mock.patch('heppy.Net.read', side_effect=ConnectionError('connection closed inside EPP frame')):
            with self.assertRaises(ConnectionError):
                epp.read()
        self.assertFalse(epp.is_connected())

    def test_request_returns_reply_with_matching_cltrid(self):
        epp = make_epp()
        reply = '<epp><response><trID><clTRID>AA-1</clTRID><svTRID>S-1</svTRID></trID></response></epp>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            self.assertEqual(reply, epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>'))
        self.assertTrue(epp.is_connected())

    def test_request_drops_connection_on_other_requests_reply(self):
        epp = make_epp()
        reply = '<epp><response><trID><clTRID>AA-0</clTRID><svTRID>S-0</svTRID></trID></response></epp>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            with self.assertRaisesRegex(ConnectionError, 'clTRID AA-0 does not match request clTRID AA-1'):
                epp.request(b'<epp><command><info/><clTRID>AA-1</clTRID></command></epp>')
        self.assertFalse(epp.is_connected())

    def test_request_accepts_greeting_as_hello_reply(self):
        epp = make_epp()
        greeting = '<epp><greeting><svID>Test</svID></greeting></epp>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=greeting):
            self.assertEqual(greeting, epp.request('<epp><hello/></epp>'))
        self.assertTrue(epp.is_connected())

    def test_request_accepts_command_reply_without_cltrid(self):
        epp = make_epp()
        reply = '<epp><response><result code="1000"/></response></epp>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            self.assertEqual(reply, epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>'))
        self.assertTrue(epp.is_connected())

    def test_request_rejects_greeting_reply_to_non_hello_command(self):
        epp = make_epp()
        greeting = '<epp><greeting><svID>Test</svID></greeting></epp>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=greeting):
            with self.assertRaisesRegex(ConnectionError, 'got a greeting in reply to a non-hello request'):
                epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>')
        self.assertFalse(epp.is_connected())

    def test_request_matches_cltrid_with_namespace_attribute(self):
        epp = make_epp()
        reply = ('<epp><response><trID>'
                 '<clTRID xmlns="urn:ietf:params:xml:ns:epp-1.0">AA-1</clTRID>'
                 '<svTRID>S-1</svTRID></trID></response></epp>')
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            self.assertEqual(reply, epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>'))
        self.assertTrue(epp.is_connected())

    def test_request_drops_connection_on_mismatched_cltrid_with_namespace_attribute(self):
        epp = make_epp()
        reply = ('<epp><response><trID>'
                 '<clTRID xmlns="urn:ietf:params:xml:ns:epp-1.0">AA-0</clTRID>'
                 '<svTRID>S-0</svTRID></trID></response></epp>')
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            with self.assertRaisesRegex(ConnectionError, 'clTRID AA-0 does not match request clTRID AA-1'):
                epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>')
        self.assertFalse(epp.is_connected())

    def test_request_timeout_names_the_request(self):
        epp = make_epp()
        epp.config = {'host': 'epp.example', 'timeout': 7}
        with mock.patch('heppy.Net.write') as write, \
                mock.patch('heppy.Net.read', side_effect=socket.timeout('timed out')) as read, \
                mock.patch('builtins.print') as out:
            with self.assertRaisesRegex(TimeoutError, r'^EPP: no reply from epp.example in 7.0s to clTRID AA-1, connection dropped$'):
                epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>')
        self.assertEqual(7.0, write.call_args.args[2])
        self.assertEqual(7.0, read.call_args.args[1])
        out.assert_called_once()
        self.assertFalse(epp.is_connected())

    def test_default_timeout_is_below_hiapi_wait(self):
        self.assertLess(make_epp().get_timeout(), 20)

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

    def test_request_reconnects_after_failed_reconnect(self):
        daemon = self.make_daemon(connected=True)
        client = daemon.client
        daemon.client = None

        def reconnect():
            daemon.client = client
        daemon.reconnect.side_effect = reconnect

        self.assertEqual('<epp/>', daemon.request('<hello/>'))
        daemon.reconnect.assert_called_once()

    def test_reconnect_keeps_start_login_overrides(self):
        daemon = Daemon.__new__(Daemon)
        daemon.login_args = {}
        daemon.connect = mock.Mock()
        daemon.login = mock.Mock()
        with mock.patch.object(Daemon, 'consume'):
            daemon.start({'login': 'override', 'pw': 'secret'})
        daemon.login.reset_mock()

        daemon.reconnect()

        daemon.login.assert_called_once_with({'login': 'override', 'pw': 'secret'})
        self.assertIsNone(daemon.login_query)


if __name__ == '__main__':
    unittest.main()
