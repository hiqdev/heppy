# -*- coding: utf-8 -*-

import unittest
from unittest import mock

from heppy import Net


class FakeSocket:
    """recv() hands out the given chunks one call at a time, then b'' (closed)."""

    def __init__(self, *chunks):
        self.chunks = list(chunks)

    def recv(self, size):
        if not self.chunks:
            return b''
        chunk = self.chunks.pop(0)
        if len(chunk) > size:
            self.chunks.insert(0, chunk[size:])
            chunk = chunk[:size]
        return chunk

    def settimeout(self, timeout):
        self.timeouts = getattr(self, 'timeouts', []) + [timeout]


def frame(xml):
    data = (xml + '\r\n').encode('utf-8')
    return Net.int_to_net(len(data) + 4) + data


class TestNetRead(unittest.TestCase):
    def test_reads_whole_frame(self):
        self.assertEqual('<epp/>', Net.read(FakeSocket(frame('<epp/>'))))

    def test_reads_header_split_across_recvs(self):
        data = frame('<epp/>')
        self.assertEqual('<epp/>', Net.read(FakeSocket(data[:1], data[1:3], data[3:])))

    def test_reads_body_split_across_recvs(self):
        data = frame('<epp>' + 'x' * 10000 + '</epp>')
        self.assertEqual('<epp>' + 'x' * 10000 + '</epp>', Net.read(FakeSocket(data[:4], data[4:100], data[100:])))

    def test_closed_before_frame_returns_empty(self):
        self.assertEqual('', Net.read(FakeSocket()))

    def test_closed_inside_header_raises(self):
        with self.assertRaises(ConnectionError):
            Net.read(FakeSocket(frame('<epp/>')[:2]))

    def test_truncated_body_raises(self):
        with self.assertRaises(ConnectionError):
            Net.read(FakeSocket(frame('<epp>truncated</epp>')[:10]))

    def test_invalid_length_raises(self):
        with self.assertRaises(ConnectionError):
            Net.read(FakeSocket(Net.int_to_net(2)))

    def test_leaves_next_frame_unread(self):
        sock = FakeSocket(frame('<first/>') + frame('<second/>'))
        self.assertEqual('<first/>', Net.read(sock))
        self.assertEqual('<second/>', Net.read(sock))



class TestNetReadTimeout(unittest.TestCase):
    def test_deadline_covers_the_whole_frame(self):
        # Each recv() is fast enough on its own, but together they take longer
        # than the timeout: a trickling reply must not get a fresh timeout per recv.
        data = frame('<epp/>')
        sock = FakeSocket(data[:4], data[4:6], data[6:])
        with mock.patch('heppy.Net.time.monotonic', side_effect=[0, 1, 9, 16]):
            with self.assertRaises(TimeoutError):
                Net.read(sock, timeout=15)

    def test_recv_gets_only_the_time_left(self):
        sock = FakeSocket(frame('<epp/>'))
        with mock.patch('heppy.Net.time.monotonic', side_effect=[100, 100, 104]):
            self.assertEqual('<epp/>', Net.read(sock, timeout=15))
        self.assertEqual([15, 11, None], sock.timeouts)

    def test_write_uses_given_timeout(self):
        sock = mock.Mock()
        Net.write(sock, '<epp/>', timeout=7)
        self.assertEqual([mock.call(7), mock.call(None)], sock.settimeout.call_args_list)


if __name__ == '__main__':
    unittest.main()
