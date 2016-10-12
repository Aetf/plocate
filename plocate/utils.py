# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import os
import mmap


class dbfile_reader(object):
    """binary file reader"""

    def __init__(self, file, encoding):
        super(dbfile_reader, self).__init__()
        self.f = mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ)
        self.encoding = encoding

    def readcstr(self):
        """Read a null-terminated string from file"""
        bytes = self.readbytestr()
        return (bytes.decode(self.encoding),
                # extra null byte is discarded, but should count
                len(bytes) + 1)

    def readbytestr(self):
        """Read a null-terminated byte string from file"""
        start = self.f.tell()
        idx = self.f.find(b'\0', start)
        if idx == -1:
            raise EOFError
        self.f.seek(idx + 1)
        return self.f[start:idx]

    def readnext(self, clz):
        """Read and parse next struct from file"""
        fmt = clz._struct
        try:
            start = self.f.tell()
            self.f.seek(fmt.size, os.SEEK_CUR)
            return clz(*fmt.unpack(self.f[start:start + fmt.size]))
        except ValueError as err:
            remain = fmt.size - (self.f.size() - self.f.tell())
            raise EOFError('File ended before get enough bytes, {} remaining'.format(remain))
