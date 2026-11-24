# -*- coding: utf-8 -*-

import unittest
from datetime import timedelta
from heppy.Daemon import Daemon, EXIT_PLANNED, EXIT_SESSION_REJECTED


class ConnectedClient:
    def is_connected(self):
        return True

    def disconnect(self):
        pass


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
