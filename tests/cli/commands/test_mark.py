# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf
import logging

import tests.support
from tests.support import mock


class MarkCommandTest(tests.support.DnfBaseTestCase):
    """Tests of ``dnf.cli.commands.MarkCommand`` class."""

    REPOS = ["main"]
    CLI = "mock"

    def setUp(self):
        super(MarkCommandTest, self).setUp()
        self.cmd = dnf.cli.commands.mark.MarkCommand(self.cli)

    @mock.patch('dnf.cli.commands.mark._',
                dnf.pycomp.NullTranslations().ugettext)
    def test_run_notfound(self):
        """Test whether it fails if the package cannot be found."""
        stdout = dnf.pycomp.StringIO()

        tests.support.command_configure(self.cmd, ['install', 'non-existent'])
        with tests.support.wiretap_logs('dnf', logging.INFO, stdout):
            with self.assertRaises(dnf.cli.CliError):
                self.cmd.run()
        self.assertEqual(stdout.getvalue(),
                         'Error:\nPackage non-existent is not installed.\n')

    @mock.patch('dnf.cli.commands.mark._',
                dnf.pycomp.NullTranslations().ugettext)
    def test_run(self):
        """Test whether it fails if the package cannot be found."""

        stdout = dnf.pycomp.StringIO()

        with tests.support.wiretap_logs('dnf', logging.INFO, stdout):
            tests.support.command_run(self.cmd, ['install', 'pepper-20-0.x86_64'])
        self.assertEqual(stdout.getvalue(),
                         'pepper-20-0.x86_64 marked as user installed.\npepper-20-0.x86_64 marked as user installed.\n')
