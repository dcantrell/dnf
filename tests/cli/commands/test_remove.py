# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import dnf.cli.commands.remove
from dnf.cli.option_parser import OptionParser

import tests.support
from tests.support import mock


class RemoveCommandTest(tests.support.ResultTestCase):
    """Tests of ``dnf.cli.commands.EraseCommand`` class."""

    REPOS = []
    BASE_CLI = True
    CLI = "mock"

    def setUp(self):
        super(RemoveCommandTest, self).setUp()
        self.cmd = dnf.cli.commands.remove.RemoveCommand(self.base.mock_cli())

    def test_configure(self):
        parser = OptionParser()
        parser.parse_main_args(['autoremove', '-y'])
        parser.parse_command_args(self.cmd, ['autoremove', '-y'])
        self.cmd.configure()
        self.assertTrue(self.cmd.cli.demands.allow_erasing)

    @mock.patch('dnf.cli.commands.remove._',
                dnf.pycomp.NullTranslations().ugettext)
    def test_run_notfound(self):
        """Test whether it fails if the package cannot be found."""
        stdout = dnf.pycomp.StringIO()

        with tests.support.wiretap_logs('dnf', logging.INFO, stdout):
            tests.support.command_run(self.cmd, ['non-existent'])
        self.assertEqual(stdout.getvalue(),
                         'No match for argument: non-existent\nNo packages marked for removal.\n')
        self.assertResult(self.cmd.base, self.cmd.base.sack.query().installed())
