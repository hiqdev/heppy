# -*- coding: utf-8 -*-
import struct
import socket
import xml.etree.ElementTree as ET

from pprint import pprint

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
def remove_bom(s):
    BOM = '\ufeff'
    if isinstance(s, bytes):
        return s.lstrip(b'\xef\xbb\xbf')
    elif isinstance(s, str):
        return s.lstrip(BOM)
    return s

def write(sock: socket, data) -> int:
    """
    Send data to socket with length prefix and CRLF suffix.
    data must be bytes.
    """
    length = int_to_net(len(data) + 4 + 2)  # 4 bytes length + 2 bytes CRLF
    sock.settimeout(20)
    sock.sendall(length)
    sended = sock.send((data if isinstance(data, bytes) else data.encode('utf-8')) + b"\r\n")
    sock.settimeout(None)
    return sended

def read(sock: socket) -> str:
    """
    Read a message from socket that is prefixed with 4 bytes length.
    Returns bytes (without trailing CRLF).
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
        return (buffer.rstrip(b"\r\n")).decode('utf-8')
    else:
        sock.settimeout(None)
        return ''

