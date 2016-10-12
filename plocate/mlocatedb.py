# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

from future.utils import native_str
import struct
import os

from . import utils


class mlocatedb(object):
    """object represents the mlocatedb"""

    class _dbheader(object):
        """database header"""
        _struct = struct.Struct(native_str('>8sIB?2x'))

        def __init__(self, magic, config_size, version, require_visibility, dbroot=None):
            super(mlocatedb._dbheader, self).__init__()
            self.magic = magic
            self.config_size = config_size
            self.version = version
            self.require_visibility = require_visibility
            self.dbroot = dbroot

    class _dirheader(object):
        """directory entry header"""
        _struct = struct.Struct(native_str('>QI4x'))

        def __init__(self, time_sec, time_nano, dirpath=None):
            super(mlocatedb._dirheader, self).__init__()
            self.time_sec = time_sec
            self.time_nano = time_nano
            self.dirpath = dirpath

    class _fileentry(object):
        """file entry"""
        _struct = struct.Struct(native_str('>B'))

        def __init__(self, kind, filename=None):
            super(mlocatedb._fileentry, self).__init__()
            self.kind = kind
            self.filename = filename

        def is_dir(self):
            return self.kind == 1

        def is_endmark(self):
            return self.kind == 2

        def is_file(self):
            return self.kind == 0

    def __init__(self, f, encoding='UTF-8'):
        super(mlocatedb, self).__init__()
        self.reader = utils.dbfile_reader(f, encoding)
        self.header = self.parse_header()
        self.config = self.parse_config()

    def __str__(self):
        return ('<mlocatedb database, version {},'
                ' require visibility {}, root {}>'.format(self.version,
                                                          self.require_visibility,
                                                          self.dbroot))

    def files(self):
        dh = self.next_dirheader()
        while dh is not None:
            fe = self.next_fileentry(dh.dirpath)
            if fe.is_endmark():
                dh = self.next_dirheader()
            else:
                yield fe

    def parse_header(self):
        """Parse a mlocate database header"""
        header = self.reader.readnext(mlocatedb._dbheader)
        if not (header.magic == b'\0mlocate' and header.version < 1):
            raise ValueError("The provided file is not in valid mlocate db format")
        header.dbroot, _ = self.reader.readcstr()
        return header

    def parse_config(self):
        done = 0
        config = {}
        key = None
        while done < self.header.config_size:
            s, read = self.reader.readcstr()
            done += read
            if key is None:
                key = s
                config[key] = []
            elif len(s) == 0:
                # this key finished
                key = None
            else:
                config[key].append(s)
        return config

    def next_dirheader(self):
        """Try parse dirheader, return None on EOF"""
        try:
            dh = self.reader.readnext(mlocatedb._dirheader)
            dh.dirpath, _ = self.reader.readcstr()
        except EOFError as err:
            return None
        return dh

    def next_fileentry(self, parentpath):
        """Parse file entry"""
        fe = self.reader.readnext(mlocatedb._fileentry)
        if fe.kind != 2:
            fe.filename = os.path.join(parentpath, self.reader.readcstr()[0])
        return fe
