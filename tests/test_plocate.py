#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
test_plocate
----------------------------------

Tests for `plocate` module.
"""


import sys
import unittest
from contextlib import contextmanager
from click.testing import CliRunner

from plocate import plocate
from plocate import cli


class Testplocate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '-h, --help                 Show this message and exit.' in help_result.output
