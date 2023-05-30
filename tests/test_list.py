# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import itertools

import libdnf.transaction

import tests.support


class List(tests.support.DnfBaseTestCase):

    REPOS = ["main", "updates"]

    def test_doPackageLists_reponame(self):
        """Test whether packages are filtered by the reponame."""
        reponame = 'main'
        lists = self.base._do_package_lists(reponame=reponame)

        pkgs = itertools.chain.from_iterable(lists.all_lists().values())
        self.assertCountEqual({pkg.reponame for pkg in pkgs}, {reponame})

        assert len(set(pkg.reponame for pkg in self.base.sack.query())) > 1, \
            ('the base must contain packages from multiple repos, '
             'otherwise the test makes no sense')

    def test_list_installed(self):
        ypl = self.base._do_package_lists('installed')
        self.assertEqual(len(ypl.installed), tests.support.TOTAL_RPMDB_COUNT)

    def test_list_installed_reponame(self):
        """Test whether only packages installed from the repository are listed."""
        expected = self.base.sack.query().installed().filter(name={'pepper', 'librita'})
        tsis = []
        for pkg in expected:
            pkg._force_swdb_repoid = "main"
            self.history.rpm.add_install(pkg)
        self._swdb_commit(tsis)

        lists = self.base._do_package_lists('installed', reponame='main')

        self.assertCountEqual(lists.installed, expected)

    def test_list_updates(self):
        ypl = self.base._do_package_lists('upgrades')
        self.assertEqual(len(ypl.updates), tests.support.UPDATES_NSOLVABLES - 2)
        pkg = ypl.updates[0]
        self.assertEqual(pkg.name, "hole")
        ypl = self.base._do_package_lists('upgrades', ["pepper"])
        self.assertEqual(len(ypl.updates), 1)
        ypl = self.base._do_package_lists('upgrades', ["mrkite"])
        self.assertEqual(len(ypl.updates), 0)

        ypl = self.base._do_package_lists('upgrades', ["hole"])
        self.assertEqual(len(ypl.updates), 1)

    def test_lists_multiple(self):
        ypl = self.base._do_package_lists('upgrades', ['pepper', 'hole'])
        self.assertLength(ypl.updates, 2)


class TestListAllRepos(tests.support.DnfBaseTestCase):

    REPOS = ["main", "updates"]

    def setUp(self):
        super(TestListAllRepos, self).setUp()
        self.base.conf.multilib_policy = "all"

    def test_list_pattern(self):
        ypl = self.base._do_package_lists('all', ['hole'])
        self.assertLength(ypl.installed, 1)
        self.assertLength(ypl.available, 2)

    def test_list_pattern_arch(self):
        ypl = self.base._do_package_lists('all', ['hole.x86_64'])
        self.assertLength(ypl.installed, 1)
        self.assertLength(ypl.available, 1)

    def test_list_available(self):
        ypl = self.base._do_package_lists('available', ['hole'], showdups=False)
        self.assertCountEqual(map(str, ypl.available), ('hole-2-1.i686',
                                                        'hole-2-1.x86_64'))

        ypl = self.base._do_package_lists('available', ['hole'], showdups=True)
        self.assertCountEqual(map(str, ypl.available), ('hole-2-1.i686',
                                                        'hole-2-1.x86_64',
                                                        'hole-1-2.x86_64'))
