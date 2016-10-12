# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import itertools


class dbfile_reader(object):
    """binary file reader"""
    def __init__(self, file, encoding):
        super(dbfile_reader, self).__init__()
        self.f = file
        self.encoding = encoding

    def readcstr(self):
        """Read a null-terminated string from file"""
        bytes = self.readbytestr()
        return (bytes.decode(self.encoding),
                # extra null byte is discarded, but should count
                len(bytes) + 1)

    def readbytestr(self):
        """Read a null-terminated byte string from file"""
        def toeof():
            byte = self.f.read(1)
            while len(byte) > 0:
                yield byte
                byte = self.f.read(1)
            raise EOFError

        return b''.join(itertools.takewhile(b'\0'.__ne__, toeof()))

    def readuntil(self, count=-1):
        """Read the file until got enough bytes, or eof"""
        def toend():
            remain = count
            byte = self.f.read(1)
            while len(byte) > 0:
                yield byte
                remain -= len(byte)
                byte = self.f.read(remain)
            if remain > 0:
                raise EOFError('File ended before get enough bytes, {} remaining'.format(remain))
        return b''.join(toend())

    def readnext(self, clz):
        """Read and parse next struct from file"""
        fmt = clz._struct
        return clz(*fmt.unpack(self.readuntil(fmt.size)))
