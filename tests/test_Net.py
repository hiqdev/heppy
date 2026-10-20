# -*- coding: utf-8 -*-

import unittest

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
        pass


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


if __name__ == '__main__':
    unittest.main()
