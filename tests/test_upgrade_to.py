# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import itertools

import dnf

import tests.support


class UpgradeTo(tests.support.ResultTestCase):

    REPOS = ['main', 'updates', 'third_party']

    def test_upgrade_to(self):
        self.base.upgrade("pepper-20-1.x86_64")
        new_set = tests.support.installed_but(self.sack, "pepper").run()
        q = self.sack.query().available()._nevra("pepper-20-1.x86_64")
        new_set.extend(q)
        self.assertResult(self.base, new_set)

    def test_upgrade_to_reponame(self):
        """Test whether only packages in selected repo are used."""
        self.base.upgrade('hole-1-2.x86_64', 'updates')

        subject = dnf.subject.Subject('hole-1-2.x86_64')
        self.assertResult(self.base, itertools.chain(
            self.sack.query().installed().filter(name__neq='hole'),
            subject.get_best_query(self.sack).filter(reponame='updates'))
        )

    def test_upgrade_to_reponame_not_in_repo(self):
        """Test whether no packages are upgraded if bad repo is selected."""
        self.base.upgrade('hole-1-2.x86_64', 'main')

        self.assertResult(self.base, self.sack.query().installed())
