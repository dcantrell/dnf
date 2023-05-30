# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

import libdnf.transaction

import dnf.cli.commands.autoremove as autoremove
from dnf.cli.option_parser import OptionParser

import tests.support


class AutoRemoveCommandTest(tests.support.ResultTestCase):

    REPOS = []
    CLI = "mock"

    def test_run(self):
        q = self.base.sack.query()
        pkgs = list(q.filter(name='librita')) + list(q.filter(name='pepper'))

        self._swdb_begin()
        for pkg in pkgs:
            self.base.history.set_reason(pkg, libdnf.transaction.TransactionItemReason_USER)
        self._swdb_end()

        cmd = autoremove.AutoremoveCommand(self.cli)
        parser = OptionParser()
        parser.parse_main_args(['autoremove', '-y'])
        parser.parse_command_args(cmd, ['autoremove', '-y'])
        cmd.run()
        inst, rem = self.installed_removed(self.base)
        self.assertEmpty(inst)
        removed = ('librita-1-1.i686',
                   'librita-1-1.x86_64',
                   'pepper-20-0.x86_64')
        self.assertCountEqual((map(str, pkgs)), removed)
