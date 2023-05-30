# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import rpm

import dnf
import dnf.goal

import tests.support
from tests.support import mock


class DowngradeTest(tests.support.ResultTestCase):

    REPOS = ["main"]
    INIT_SACK = True

    @mock.patch('dnf.rpm.transaction.TransactionWrapper')
    def test_package_downgrade(self, ts):
        pkgs = self.base.add_remote_rpms([tests.support.TOUR_44_PKG_PATH])
        cnt = self.base.package_downgrade(pkgs[0])
        self.base._ts.setProbFilter.assert_called_with(
            rpm.RPMPROB_FILTER_OLDPACKAGE)
        self.assertGreater(cnt, 0)
        (installed, removed) = self.installed_removed(self.base)
        self.assertCountEqual(map(str, installed), ("tour-4-4.noarch", ))
        self.assertCountEqual(map(str, removed), ("tour-5-0.noarch", ))

    def test_downgrade(self):
        cnt = self.base.downgrade("tour")
        self.assertGreater(cnt, 0)

        new_pkg = self.base.sack.query().available().filter(name="tour")[0]
        self.assertEqual(new_pkg.evr, "4.6-1")
        new_set = tests.support.installed_but(self.base.sack, "tour") + [new_pkg]
        self.assertResult(self.base, new_set)

    def test_downgrade2(self):
        # override base with custom repos
        self.base = tests.support.MockBase("old_versions")
        self.base.downgrade("tour")
        installed, removed = self.installed_removed(self.base)
        self.assertCountEqual(map(str, installed), ['tour-4.9-1.noarch'])
        self.assertCountEqual(map(str, removed), ['tour-5-0.noarch'])


class DowngradeTest2(tests.support.DnfBaseTestCase):

    REPOS = ["main"]
    INIT_SACK = True

    def setUp(self):
        super(DowngradeTest2, self).setUp()
        self.base._goal = mock.create_autospec(dnf.goal.Goal)

    def test_downgrade_pkgnevra(self):
        """ Downgrade should handle full NEVRAs. """
        tests.support.ObjectMatcher(dnf.package.Package, {'name': 'tour'})
        with self.assertRaises(dnf.exceptions.PackagesNotInstalledError):
            self.base.downgrade('tour-0:5-0.noarch')

    def test_downgrade_notinstalled(self):
        pkg = tests.support.ObjectMatcher(dnf.package.Package, {'name': 'lotus'})

        with self.assertRaises(dnf.exceptions.PackagesNotInstalledError) as context:
            self.base.downgrade('lotus')
        self.assertEqual(context.exception.pkg_spec, 'lotus')
        self.assertEqual(tuple(context.exception.packages), (pkg,) * 2)
        self.assertEqual(self.goal.mock_calls, [])

    def test_downgrade_notfound(self):
        with self.assertRaises(dnf.exceptions.PackageNotFoundError) as context:
            self.base.downgrade('non-existent')
        self.assertEqual(context.exception.pkg_spec, 'non-existent')
        self.assertEqual(self.goal.mock_calls, [])

    def test_downgrade_nodowngrade(self):
        downgraded_count = self.base.downgrade('pepper')

        self.assertEqual(self.goal.mock_calls, [])
        self.assertEqual(downgraded_count, 0)
