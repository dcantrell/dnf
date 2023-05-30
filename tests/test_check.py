# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import dnf.cli.commands.check
import dnf.pycomp

import tests.support


EXPECTED_DUPLICATES_FORMAT = """\
dup-1-0.noarch is a duplicate with dup-2-0.noarch
dup-1-0.noarch is a duplicate with dup-3-0.noarch
"""

EXPECTED_OBSOLETED_FORMAT = """\
test-1-0.noarch is obsoleted by obs-3-0.noarch
"""


class CheckDuplicatesTest(tests.support.DnfBaseTestCase):

    REPOS = []
    BASE_CLI = True
    CLI = "stub"

    def test_duplicates(self):
        self.cmd = dnf.cli.commands.check.CheckCommand(self.cli)
        tests.support.command_configure(self.cmd, ['--duplicates'])
        with tests.support.patch_std_streams() as (stdout, _):
            with self.assertRaises(dnf.exceptions.Error) as ctx:
                self.cmd.run()
            self.assertEqual(str(ctx.exception),
                             'Check discovered 2 problem(s)')
        self.assertEqual(stdout.getvalue(), EXPECTED_DUPLICATES_FORMAT)

    def test_obsoleted(self):
        self.cmd = dnf.cli.commands.check.CheckCommand(self.cli)
        tests.support.command_configure(self.cmd, ['--obsoleted'])
        with tests.support.patch_std_streams() as (stdout, _):
            with self.assertRaises(dnf.exceptions.Error) as ctx:
                self.cmd.run()
            self.assertEqual(str(ctx.exception),
                             'Check discovered 1 problem(s)')
        self.assertEqual(stdout.getvalue(), EXPECTED_OBSOLETED_FORMAT)
