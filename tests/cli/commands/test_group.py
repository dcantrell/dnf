# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

import dnf.cli.commands.group as group
import dnf.comps
import dnf.exceptions
from dnf.comps import CompsQuery
from dnf.cli.option_parser import OptionParser

import tests.support


class GroupCommandStaticTest(tests.support.TestCase):

    def test_canonical(self):
        cmd = group.GroupCommand(tests.support.mock.MagicMock())

        for args, out in [
                (['grouplist', 'crack'], ['list', 'crack']),
                (['groups'], ['summary']),
                (['group', 'info', 'crack'], ['info', 'crack']),
                (['group', 'update', 'crack'], ['upgrade', 'crack'])]:
            parser = OptionParser()
            parser.parse_main_args(args)
            parser.parse_command_args(cmd, args)
            cmd._canonical()
            self.assertEqual(cmd.opts.subcmd, out[0])
            self.assertEqual(cmd.opts.args, out[1:])

    def test_split_extcmds(self):
        cmd = group.GroupCommand(tests.support.mock.MagicMock())
        cmd.base.conf = dnf.conf.Conf()
        tests.support.command_run(cmd, ['install', 'crack'])
        cmd.base.env_group_install.assert_called_with(
            ['crack'], ('mandatory', 'default', 'conditional'),
            cmd.base.conf.strict)


class GroupCommandTest(tests.support.DnfBaseTestCase):

    REPOS = ["main"]
    COMPS = True
    INIT_SACK = True

    def setUp(self):
        super(GroupCommandTest, self).setUp()
        self.cmd = group.GroupCommand(self.base.mock_cli())
        self.parser = OptionParser()

    def test_environment_list(self):
        env_inst, env_avail = self.cmd._environment_lists(['sugar*'])
        self.assertLength(env_inst, 0)
        self.assertLength(env_avail, 1)
        self.assertEqual(env_avail[0].name, 'Sugar Desktop Environment')

    def test_configure(self):
        tests.support.command_configure(self.cmd, ['remove', 'crack'])
        demands = self.cmd.cli.demands
        self.assertTrue(demands.allow_erasing)
        self.assertFalse(demands.freshest_metadata)


class CompsQueryTest(tests.support.DnfBaseTestCase):

    REPOS = []
    COMPS = True

    def test_all(self):
        status_all = CompsQuery.AVAILABLE | CompsQuery.INSTALLED
        kinds_all = CompsQuery.ENVIRONMENTS | CompsQuery.GROUPS
        q = CompsQuery(self.comps, self.history, kinds_all, status_all)

        res = q.get('sugar*', '*er*')
        self.assertCountEqual(res.environments,
                              ('sugar-desktop-environment',))
        self.assertCountEqual(res.groups, ("Peppers", 'somerset'))

    def test_err(self):
        q = CompsQuery(self.comps, self.history, CompsQuery.ENVIRONMENTS,
                       CompsQuery.AVAILABLE)
        with self.assertRaises(dnf.exceptions.CompsError):
            q.get('*er*')

    def test_installed(self):
        q = CompsQuery(self.comps, self.history, CompsQuery.GROUPS,
                       CompsQuery.INSTALLED)
        self.base.read_mock_comps(False)
        grp = self.base.comps.group_by_pattern('somerset')
        self.base.group_install(grp.id, ('mandatory',))

        self._swdb_commit()

        res = q.get('somerset')
        self.assertEmpty(res.environments)
        grp_ids = list(res.groups)
        self.assertCountEqual(grp_ids, ('somerset',))
