# -*- coding: utf-8 -*-

import struct

from typing import Union
from socket import socket
from heppy.Error import Error
from heppy.Request import Request

# http://www.bortzmeyer.org/4934.html
def format_32():
    # Get the size of C integers. We need 32 bits unsigned.
    format_32 = ">I"
    if struct.calcsize(format_32) < 4:
        format_32 = ">L"
        if struct.calcsize(format_32) != 4:
            raise Exception("Cannot find a 32 bits integer")
    elif struct.calcsize(format_32) > 4:
        format_32 = ">H"
        if struct.calcsize(format_32) != 4:
            raise Exception("Cannot find a 32 bits integer")
    return format_32

FORMAT_32 = format_32()

def int_from_net(data: bytes) -> int:
    return struct.unpack(FORMAT_32, data)[0]

def int_to_net(value: int) -> bytes:
    return struct.pack(FORMAT_32, value)

# Remove BOM from a string (works for both str and bytes)
def remove_bom(s: Union[bytes, str]):
    BOM = '\ufeff'
    if isinstance(s, bytes):
        return s.lstrip(b'\xef\xbb\xbf')
    elif isinstance(s, str):
        return s.lstrip(BOM)
    return s

def write(sock: socket, data: Union[bytes, str]) -> int:
    """
    Send data to socket with length prefix and CRLF suffix.
    data must be bytes or str.
    Returns number of bytes sent (including length prefix)
    """
    if sock is None:
        raise Error('Connection lost to registry or not connected')
    if not isinstance(data, (bytes, str)):
        raise Error("Data must be bytes or str", {"data": data})
    data = remove_bom(data)  # Remove BOM if present
    if isinstance(data, bytes):
        data = data.decode('utf-8')  # Convert bytes to str if necessary
    if not data.endswith('\r\n'):
        data += '\r\n'
    data_bytes = data.encode('utf-8')
    length = int_to_net(len(data_bytes) + 4)  # 4 bytes length
    sock.settimeout(20)
    try:
        sock.sendall(length)
        sock.sendall(data_bytes)
    finally:
        sock.settimeout(None)
    return length

def recv_exactly(sock: socket, size: int) -> bytes:
    """
    Read exactly size bytes, fewer only if the peer closes the connection.
    A single recv() may return less than asked (TLS records, TCP segments).
    """
    buffer = b''
    while len(buffer) < size:
        chunk = sock.recv(min(4096, size - len(buffer)))
        if not chunk:
            break
        buffer += chunk
    return buffer

def read(sock: socket) -> str:
    """
    Read a message from socket that is prefixed with 4 bytes length.
    Returns string (without trailing CRLF), or '' if the peer closed the
    connection before sending anything.
    Raises ConnectionError (an OSError) when the connection ends inside a
    frame: the rest of the stream can't be trusted to line up with the next
    request any more.
    """
    if sock is None:
        raise Error('Connection lost to registry or not connected')
    sock.settimeout(20)
    try:
        net = recv_exactly(sock, 4)
        if not net:
            return ''
        if len(net) < 4:
            raise ConnectionError('connection closed inside EPP frame header (%d of 4 bytes)' % len(net))
        length = int_from_net(net) - 4
        if length < 0:
            raise ConnectionError('invalid EPP frame length %d' % (length + 4))
        buffer = recv_exactly(sock, length)
        if len(buffer) < length:
            raise ConnectionError('connection closed inside EPP frame (%d of %d bytes)' % (len(buffer), length))
    finally:
        sock.settimeout(None)
    return (buffer.rstrip(b"\r\n")).decode('utf-8')
