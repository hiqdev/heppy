# -*- coding: utf-8 -*-

import struct
import socket
import xml.etree.ElementTree as ET

from typing import Union
from socket import socket
from pprint import pprint
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
    sock.sendall(length)
    sent = sock.sendall(data_bytes)
    sock.settimeout(None)
    return length if sent is None else 0

def read(sock: socket) -> str:
    """
    Read a message from socket that is prefixed with 4 bytes length.
    Returns string (without trailing CRLF).
    """
    sock.settimeout(20)
    net = sock.recv(4)
    if net:
        length = int_from_net(net) - 4
        buffer = b''
        while length > len(buffer):
            chunk = sock.recv(min(4096, length - len(buffer)))
            if not chunk:
                break
            buffer += chunk
        sock.settimeout(None)
        answer = (buffer.rstrip(b"\r\n")).decode('utf-8')
        return answer
    else:
        sock.settimeout(None)
        return ''

