# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, division, print_function

import itertools
import os
import re

from . import mlocatedb


def locate(patterns, database, **options):
    flags = re.IGNORECASE if options['ignore_case'] else 0
    regs = [re.compile(pt, flags) for pt in patterns]

    def predict(fe):
        if options['type'] == 'file' and not fe.is_file():
            return False
        elif options['type'] == 'dir' and not fe.is_dir():
            return False
        elif fe.is_endmark():
            return False
        else:
            if options['existing']:
                exist_test = os.path.exists if options['follow'] else os.path.lexists
                if not exist_test(fe.filename):
                    return False

            if options['match'] == 'wholename':
                pathname = fe.filename
            elif options['match'] == 'basename':
                pathname = os.path.basename(fe.filename)
            else:
                raise ValueError('Unknown value for option \'match\': {}'.format(options['match']))

            res = [reg.search(pathname) is not None for reg in regs]

            if options['all']:
                return all(res)
            else:
                return any(res)

    mdb = mlocatedb.mlocatedb(database)
    reslist = itertools.islice((fe.filename for fe in mdb.files() if predict(fe)),
                               options['limit'])
    return reslist
