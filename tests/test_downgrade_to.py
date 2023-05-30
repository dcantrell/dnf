# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf

import tests.support


class DowngradeTo(tests.support.ResultTestCase):

    REPOS = ['main', 'old_versions']

    def test_downgrade_to_lowest(self):
        with tests.support.mock.patch('logging.Logger.warning'):
            with self.assertRaises(dnf.exceptions.PackagesNotInstalledError):
                self.base.downgrade_to('hole')
        self.assertResult(self.base, self.base._sack.query().installed())

    def test_downgrade_to_name(self):
        self.base.downgrade_to('tour')
        (installed, removed) = self.installed_removed(self.base)
        self.assertCountEqual(map(str, installed),
                              ('tour-4.9-1.noarch',))
        self.assertCountEqual(map(str, removed),
                              ('tour-5-0.noarch',))

    def test_downgrade_to_wildcard_name(self):
        self.base.downgrade_to('tour*')
        (installed, removed) = self.installed_removed(self.base)
        self.assertCountEqual(map(str, installed),
                              ('tour-4.9-1.noarch',))
        self.assertCountEqual(map(str, removed),
                              ('tour-5-0.noarch',))

    def test_downgrade_to_version(self):
        self.base.downgrade_to('tour-4.6')
        (installed, removed) = self.installed_removed(self.base)
        self.assertCountEqual(map(str, installed),
                              ('tour-4.6-1.noarch',))
        self.assertCountEqual(map(str, removed),
                              ('tour-5-0.noarch',))
