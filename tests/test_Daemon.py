# -*- coding: utf-8 -*-

import io
import sys
import unittest
from datetime import timedelta
from unittest import mock
from heppy.Daemon import Daemon, EXIT_PLANNED, EXIT_SESSION_REJECTED


class ConnectedClient:
    def is_connected(self):
        return True

    def disconnect(self):
        pass


class FakeClient:
    """Client that records calls; connected tells what is_connected() reports."""

    def __init__(self, connected):
        self.connected = connected
        self.disconnected = False

    def is_connected(self):
        return self.connected

    def disconnect(self):
        self.disconnected = True
        self.connected = False


def unexpected_request(query):
    raise AssertionError('no request expected, got %r' % query)


def closed_connection(query):
    raise ConnectionError('closed the connection without a reply, connection dropped')


class TestDaemon(unittest.TestCase):
    def make_daemon(self, hello_reply=None):
        daemon = Daemon({}, {})
        daemon.smart_request = lambda query: hello_reply
        return daemon

    def assert_exits_with(self, code, daemon):
        with self.assertRaises(SystemExit) as raised:
            daemon.recheck()
        self.assertEqual(code, raised.exception.code)

    def test_forcequit_exits_planned(self):
        daemon = self.make_daemon()
        daemon.started -= daemon.forcequitDelta + timedelta(seconds=1)
        self.assert_exits_with(EXIT_PLANNED, daemon)

    def test_signal_quit_exits_planned(self):
        daemon = self.make_daemon()
        with self.assertRaises(SystemExit) as raised:
            daemon.quit()
        self.assertEqual(EXIT_PLANNED, raised.exception.code)

    def test_forcequit_exits_planned_when_logout_finds_connection_closed(self):
        daemon = self.make_daemon()
        daemon.client = ConnectedClient()
        daemon.request = closed_connection
        daemon.started -= daemon.forcequitDelta + timedelta(seconds=1)
        self.assert_exits_with(EXIT_PLANNED, daemon)

    def test_forcequit_exits_planned_when_logout_times_out(self):
        daemon = self.make_daemon()
        daemon.client = FakeClient(connected=True)

        def timed_out(query):
            raise TimeoutError('EPP: no reply in 15.0s, connection dropped')

        daemon.request = timed_out
        daemon.started -= daemon.forcequitDelta + timedelta(seconds=1)
        self.assert_exits_with(EXIT_PLANNED, daemon)
        self.assertTrue(daemon.client.disconnected)

    def test_quit_logs_out_and_disconnects_a_live_session(self):
        daemon = self.make_daemon()
        daemon.client = FakeClient(connected=True)
        sent = []
        daemon.request = sent.append
        with self.assertRaises(SystemExit) as raised:
            daemon.quit()
        self.assertEqual(EXIT_PLANNED, raised.exception.code)
        self.assertEqual(1, len(sent))
        self.assertIn('logout', str(sent[0]))
        self.assertTrue(daemon.client.disconnected)

    def test_quit_on_dropped_connection_neither_reconnects_nor_logs_in(self):
        daemon = self.make_daemon()
        daemon.client = FakeClient(connected=False)
        daemon.request = unexpected_request
        daemon.reconnect = lambda: self.fail('quit must not reconnect')
        daemon.login = lambda args=None: self.fail('quit must not log in')
        with self.assertRaises(SystemExit) as raised:
            daemon.quit()
        self.assertEqual(EXIT_PLANNED, raised.exception.code)

    def test_cli_quit_with_args_exits_planned(self):
        daemon = self.make_daemon()
        with self.assertRaises(SystemExit) as raised:
            daemon.quit({'command': 'quit', 'path': 'epp.json'})
        self.assertEqual(EXIT_PLANNED, raised.exception.code)

    def test_quit_keeps_exit_code_when_stdout_is_closed(self):
        daemon = self.make_daemon()
        closed = io.StringIO()
        closed.close()
        with mock.patch.object(sys, 'stdout', closed):
            with self.assertRaises(SystemExit) as raised:
                daemon.quit(EXIT_SESSION_REJECTED)
        self.assertEqual(EXIT_SESSION_REJECTED, raised.exception.code)

    def test_rejected_hello_exits_session_rejected(self):
        daemon = self.make_daemon({'result_code': '2500'})
        daemon.force_hello = True
        self.assert_exits_with(EXIT_SESSION_REJECTED, daemon)

    def test_accepted_hello_keeps_running(self):
        daemon = self.make_daemon({'svID': 'test'})
        daemon.force_hello = True
        daemon.recheck()


if __name__ == '__main__':
    unittest.main()
