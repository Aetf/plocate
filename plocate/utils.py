# -*- coding: utf-8 -*-

import itertools


def readcstr(f):
    """Read a null-terminated byte string from file"""
    def toeof():
        byte = f.read(1)
        while len(byte) > 0:
            yield byte
            byte = f.read(1)
        raise EOFError

    return b''.join(itertools.takewhile(b'\0'.__ne__, toeof()))


def readuntil(f, count=-1):
    """Read the file until got enough bytes, or eof"""
    def toend():
        remain = count
        byte = f.read(1)
        while len(byte) > 0:
            yield byte
            remain -= len(byte)
            byte = f.read(remain)
        if remain > 0:
            raise EOFError('File ended before get enough bytes, {} remaining'.format(remain))
    return b''.join(toend())

def readnext(f, fmt):
    """Read and parse next struct from file"""
    return fmt.unpack(readuntil(f, fmt.size))
