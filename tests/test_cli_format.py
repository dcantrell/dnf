# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.cli.format
from dnf.cli.format import format_time, format_number

import tests.support


class FormatTest(tests.support.TestCase):
    def test_format_time(self):
        self.assertEqual(format_time(None), '--:--')
        self.assertEqual(format_time(-1), '--:--')
        self.assertEqual(format_time(12 * 60 + 34), '12:34')
        self.assertEqual(format_time(12 * 3600 + 34 * 60 + 56), '754:56')
        self.assertEqual(format_time(12 * 3600 + 34 * 60 + 56, use_hours=True), '12:34:56')

    def test_format_number(self):
        self.assertEqual(format_number(None), '0.0  ')
        self.assertEqual(format_number(-1), '-1  ')
        self.assertEqual(format_number(1.0), '1.0  ')
        self.assertEqual(format_number(999.0), '999  ')
        self.assertEqual(format_number(1000.0), '1.0 k')
        self.assertEqual(format_number(1 << 20), '1.0 M')
        self.assertEqual(format_number(1 << 30), '1.0 G')
        self.assertEqual(format_number(1e6, SI=1), '1.0 M')
        self.assertEqual(format_number(1e9, SI=1), '1.0 G')

    def test_indent_block(self):
        s = 'big\nbrown\nbag'
        out = dnf.cli.format.indent_block(s)
        self.assertEqual(out, '  big\n  brown\n  bag')
