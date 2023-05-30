# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import rpm

import tests.support


class DistroSyncAll(tests.support.ResultTestCase):

    REPOS = ["distro"]
    INIT_SACK = True

    def test_distro_sync_all(self):
        self.base.distro_sync()
        self.assertIn(rpm.RPMPROB_FILTER_OLDPACKAGE, self.base._rpm_probfilter)
        packages = tests.support.installed_but(self.sack, "pepper", "librita").run()
        q = self.sack.query().available().filter(name=["pepper", "librita"])
        packages.extend(q)
        self.assertResult(self.base, packages)


class DistroSync(tests.support.ResultTestCase):

    REPOS = ["main", "updates"]
    BASE_CLI = True

    def test_distro_sync(self):
        installed = self._get_installed(self.base)
        original_pkg = list(filter(lambda p: p.name == "hole", installed))
        self.base.distro_sync_userlist(('bla', 'hole'))
        obsolete_pkg = list(filter(lambda p: p.name == "tour", installed))

        installed2 = self._get_installed(self.base)
        updated_pkg = list(filter(lambda p: p.name == "hole", installed2))
        self.assertLength(updated_pkg, 1)
        self.assertLength(original_pkg, 1)
        self.assertLength(updated_pkg, 1)

        # holy pkg upgraded from version 1 to 2 and obsoletes tour
        self.assertEqual(original_pkg[0].version, "1")
        self.assertEqual(updated_pkg[0].version, "2")
        installed.remove(original_pkg[0])
        installed.remove(obsolete_pkg[0])
        installed2.remove(updated_pkg[0])
        self.assertEqual(installed, installed2)
