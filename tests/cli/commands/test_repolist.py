# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

import dnf.cli.commands.repolist as repolist
import dnf.repo

import tests.support


class TestRepolist(tests.support.TestCase):

    @tests.support.mock.patch('dnf.cli.commands.repolist._',
                              dnf.pycomp.NullTranslations().ugettext)
    def test_expire_str(self):
        repo = dnf.repo.Repo('rollup', tests.support.FakeConf())
        expire = repolist._expire_str(repo, None)
        self.assertEqual(expire, '172800 second(s) (last: unknown)')
