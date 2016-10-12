# -*- coding: utf-8 -*-

import functools
import struct

from . import utils


class mlocatedb(object):
    """object represents the mlocatedb"""

    class _dbheader(object):
        """database header"""
        _struct = struct.Struct('>8sIB?2x')

        def __init__(self, magic, config_size, version, require_visibility, dbroot=None):
            super(mlocatedb._dbheader, self).__init__()
            self.magic = magic
            self.config_size = config_size
            self.version = version
            self.require_visibility = require_visibility
            self.dbroot = dbroot

    class _dirheader(object):
        """directory entry header"""
        _struct = struct.Struct('>QI4x')

        def __init__(self, time_sec, time_nano, dirpath=None):
            super(mlocatedb._dirheader, self).__init__()
            self.time_sec = time_sec
            self.time_nano = time_nano
            self.dirpath = dirpath

    class _fileentry(object):
        """file entry"""
        _struct = struct.Struct('>B')

        def __init__(self, kind, filename=None):
            super(mlocatedb._fileentry, self).__init__()
            self.kind = kind
            self.filename = filename

        def is_dir(self):
            return self.kind == 1

        def is_endmark(self):
            return self.kind == 3

        def is_file(self):
            return self.kind == 0

    def __init__(self, f, encoding='UTF-8'):
        super(mlocatedb, self).__init__()
        self.header = parse_header(f, encoding)
        self.config = parse_config(f, self.header.config_size, encoding)

        self.files = []
        dh = parse_dirheader(f, encoding)
        while dh is not None:
            fe = parse_fileentry(f, dh.dirpath, encoding)
            self.files.append(fe)

    def __str__(self):
        return ('<mlocatedb database, version {},'
                ' require visibility {}, root {}>'.format(self.version,
                                                          self.require_visibility,
                                                          self.dbroot))


def parse_header(file, encoding):
    """Parse a mlocate database"""
    header = mlocatedb._dbheader(*utils.readnext(file, mlocatedb._dbheader._struct))
    if not (header.magic == b'\0mlocate' and header.version < 1):
        raise ValueError("The provided file is not in valid mlocate db format")
    header.dbroot = utils.readcstr(file).decode(encoding)
    return header


def parse_config(file, size, encoding):
    done = 0
    config = {}
    key = None
    while done < size:
        s = utils.readcstr(file)
        # extra null byte is discarded, but should count
        done += len(s) + 1
        if key is None:
            key = s.decode(encoding)
            config[key] = []
        elif len(s) == 0:
            # this key finished
            key = None
        else:
            value = s.decode(encoding)
            config[key].append(value)
    return config


def parse_dirheader(file, encoding):
    """Try parse dirheader, return None on EOF"""
    try:
        dh = mlocatedb._dirheader(*utils.readnext(file, mlocatedb._dirheader._struct))
        dh.dirpath = utils.readcstr(file).decode(encoding)
    except EOFError as err:
        return None
    return dh


def parse_fileentry(file, parentpath, encoding):
    """Parse file entry"""
    fe = mlocatedb._fileentry(*utils.readnext(file, mlocatedb._fileentry._struct))
    if fe.kind != 2:
        fe.filename = parentpath + '/' + utils.readcstr(file).decode(encoding)
    return fe
