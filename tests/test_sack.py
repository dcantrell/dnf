# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.exceptions
import dnf.repo
import dnf.sack

import tests.support
from tests.support import mock


class SackTest(tests.support.DnfBaseTestCase):

    REPOS = []

    def test_excludepkgs(self):
        self.base.conf.excludepkgs = ['pepper']
        self.base._setup_excludes_includes()
        peppers = self.base.sack.query().filter(name='pepper').run()
        self.assertLength(peppers, 0)

    def test_exclude(self):
        self.base.conf.exclude = ['pepper']
        self.base._setup_excludes_includes()
        peppers = self.base.sack.query().filter(name='pepper').run()
        self.assertLength(peppers, 0)

    def test_disable_excludes(self):
        self.base.conf.disable_excludes = ['all']
        self.base.conf.excludepkgs = ['pepper']
        self.base._setup_excludes_includes()
        peppers = self.base.sack.query().filter(name='pepper').run()
        self.assertLength(peppers, 1)

    def test_excludepkgs_glob(self):
        # override base with custom repos
        self.base = tests.support.MockBase('main')
        self.base.repos['main'].excludepkgs = ['pepp*']
        self.base._setup_excludes_includes()
        peppers = self.base.sack.query().filter(name='pepper', reponame='main')
        self.assertLength(peppers, 0)

    def test_excludepkgs_includepkgs(self):
        self.base.conf.excludepkgs = ['*.i?86']
        self.base.conf.includepkgs = ['lib*']
        self.base._setup_excludes_includes()
        peppers = self.base.sack.query().run()
        self.assertLength(peppers, 1)
        self.assertEqual(str(peppers[0]), "librita-1-1.x86_64")

    @mock.patch('dnf.sack._build_sack', lambda x: mock.Mock())
    @mock.patch('dnf.goal.Goal', lambda x: mock.Mock())
    def test_fill_sack(self):
        def raiser():
            raise dnf.exceptions.RepoError()

        r = tests.support.MockRepo('bag', self.base.conf)
        r.enable()
        self.base._repos.add(r)
        r.load = mock.Mock(side_effect=raiser)
        r.skip_if_unavailable = False
        self.assertRaises(dnf.exceptions.RepoError,
                          self.base.fill_sack, load_system_repo=False)
        self.assertTrue(r.enabled)
        self.assertTrue(r._check_config_file_age)
