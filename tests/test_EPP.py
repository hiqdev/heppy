# -*- coding: utf-8 -*-

import ssl
import socket
import unittest
from datetime import datetime, timedelta
from unittest import mock

from heppy.EPP import EPP, REPP, is_read_only
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

    def test_request_drops_connection_on_malformed_reply(self):
        epp = make_epp()
        reply = '<epp><response><trID><clTRID>AA-1</clTRID>'
        with mock.patch('heppy.Net.write'), mock.patch('heppy.Net.read', return_value=reply):
            with self.assertRaisesRegex(ConnectionError, 'malformed XML reply'):
                epp.request('<epp><command><info/><clTRID>AA-1</clTRID></command></epp>')
        self.assertFalse(epp.is_connected())

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


class TestREPP(unittest.TestCase):
    def make_repp(self, replies):
        repp = REPP.__new__(REPP)
        repp.config = {'host': 'epp.example'}
        repp.epp = make_epp()
        repp.epp.request = mock.Mock(side_effect=replies)
        repp.connect = mock.Mock()
        return repp

    def test_request_without_a_reply_drops_the_connection_without_opening_another(self):
        repp = self.make_repp([''])
        with self.assertRaisesRegex(ConnectionError, r'^EPP: epp.example closed the connection without a reply, connection dropped$'):
            repp.request('<hello/>')
        self.assertFalse(repp.is_connected())
        repp.connect.assert_not_called()

    def test_request_returns_the_reply(self):
        repp = self.make_repp(['<epp/>'])
        self.assertEqual('<epp/>', repp.request('<hello/>'))
        repp.connect.assert_not_called()


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


class TestDaemonRetry(unittest.TestCase):
    INFO = '<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><command><info><domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0"><domain:name>example.com</domain:name></domain:info></info><clTRID>c1</clTRID></command></epp>'
    CREATE = '<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><command><create><domain:create xmlns:domain="urn:ietf:params:xml:ns:domain-1.0"><domain:name>example.com</domain:name></domain:create></create><clTRID>c2</clTRID></command></epp>'

    def make_daemon(self, replies):
        daemon = Daemon.__new__(Daemon)
        daemon.handler = mock.MagicMock()
        daemon.client = mock.Mock(spec=REPP)
        daemon.client.is_connected.return_value = True
        daemon.client.request.side_effect = replies
        daemon.reconnect = mock.Mock()
        return daemon

    def test_read_only_request_is_retried_on_a_new_logged_in_connection(self):
        daemon = self.make_daemon([ConnectionError('no reply'), '<epp/>'])
        self.assertEqual('<epp/>', daemon.request(self.INFO))
        daemon.reconnect.assert_called_once()
        self.assertEqual(2, daemon.client.request.call_count)

    def test_read_only_request_is_retried_only_once(self):
        daemon = self.make_daemon([ConnectionError('no reply'), ConnectionError('no reply again')])
        with self.assertRaisesRegex(ConnectionError, 'no reply again'):
            daemon.request(self.INFO)
        daemon.reconnect.assert_called_once()

    def test_other_request_is_not_retried(self):
        daemon = self.make_daemon([ConnectionError('no reply'), '<epp/>'])
        with self.assertRaises(ConnectionError):
            daemon.request(self.CREATE)
        daemon.reconnect.assert_not_called()
        self.assertEqual(1, daemon.client.request.call_count)

    def test_timeout_is_not_retried(self):
        daemon = self.make_daemon([TimeoutError('no reply in 15s'), '<epp/>'])
        with self.assertRaises(TimeoutError):
            daemon.request(self.INFO)
        daemon.reconnect.assert_not_called()


class TestDaemonSessionCheck(unittest.TestCase):
    def make_daemon(self, reply, interval=None):
        daemon = Daemon.__new__(Daemon)
        daemon.sessionCheckDelta = timedelta(**(interval if interval is not None else {'minutes': 5}))
        daemon.last_session_check = datetime.now() - timedelta(minutes=6)
        daemon.smart_request = mock.Mock(return_value=reply)
        daemon.reconnect = mock.Mock()
        return daemon

    def test_due_after_interval(self):
        daemon = self.make_daemon({})
        self.assertTrue(daemon.needs_session_check())
        daemon.last_session_check = datetime.now()
        self.assertFalse(daemon.needs_session_check())

    def test_disabled_with_zero_interval(self):
        self.assertFalse(self.make_daemon({}, interval={}).needs_session_check())

    def test_live_session_is_kept(self):
        for code in ['1300', '1301']:
            daemon = self.make_daemon({'result_code': code})
            daemon.check_session()
            daemon.smart_request.assert_called_once_with({'command': 'epp:poll', 'op': 'req'})
            daemon.reconnect.assert_not_called()
            self.assertFalse(daemon.needs_session_check())

    def test_refused_poll_reconnects(self):
        daemon = self.make_daemon({'result_code': '2201', 'result_msg': 'Authorization error'})
        daemon.check_session()
        daemon.reconnect.assert_called_once()

    def test_lost_connection_is_left_to_the_next_request(self):
        daemon = self.make_daemon({'_error': 'EPP: no reply'})
        daemon.check_session()
        daemon.reconnect.assert_not_called()

    def test_failed_reconnect_does_not_raise(self):
        daemon = self.make_daemon({'result_code': '2201'})
        daemon.reconnect.side_effect = OSError('registry down')
        daemon.check_session()
        daemon.reconnect.assert_called_once()


class TestIsReadOnly(unittest.TestCase):
    def wrap(self, command):
        return '<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><command>%s<clTRID>x</clTRID></command></epp>' % command

    def test_read_only(self):
        self.assertTrue(is_read_only('<epp xmlns="urn:ietf:params:xml:ns:epp-1.0"><hello/></epp>'))
        self.assertTrue(is_read_only(self.wrap('<check/>')))
        self.assertTrue(is_read_only(self.wrap('<info/>')))
        self.assertTrue(is_read_only(self.wrap('<poll op="req"/>')))
        self.assertTrue(is_read_only(self.wrap('<transfer op="query"/>')))

    def test_not_read_only(self):
        for command in ['<create/>', '<renew/>', '<update/>', '<delete/>', '<login/>', '<logout/>',
                        '<poll op="ack" msgID="1"/>', '<transfer op="request"/>', '<transfer op="approve"/>']:
            self.assertFalse(is_read_only(self.wrap(command)), command)
        self.assertFalse(is_read_only(''))
        self.assertFalse(is_read_only('not xml'))

    def test_read_only_with_extension(self):
        self.assertTrue(is_read_only(self.wrap('<info/><extension/>')))

    def test_not_read_only_with_more_than_one_operation(self):
        for command in ['<info/><update/>', '<update/><info/>', '<check/><info/>', '<poll op="req"/><create/>']:
            self.assertFalse(is_read_only(self.wrap(command)), command)

    def test_not_read_only_without_operation(self):
        self.assertFalse(is_read_only(self.wrap('')))

    def test_not_read_only_with_more_than_one_top_level_element(self):
        epp = '<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">%s</epp>'
        for elements in ['<command><info/></command><command><update/></command>',
                         '<hello/><command><update/></command>',
                         '<command><info/></command><hello/>']:
            self.assertFalse(is_read_only(epp % elements), elements)


if __name__ == '__main__':
    unittest.main()
