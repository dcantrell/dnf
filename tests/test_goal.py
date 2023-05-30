# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import libdnf.transaction

import dnf.goal
import dnf.selector

import tests.support


class GoalTest(tests.support.DnfBaseTestCase):

    REPOS = ['main']
    INIT_SACK = True

    def test_get_reason(self):
        sltr = dnf.selector.Selector(self.sack)
        sltr.set(name='mrkite')
        grp_sltr = dnf.selector.Selector(self.sack)
        grp_sltr.set(name='lotus')

        self.goal.install(select=sltr)
        self.goal.install(select=grp_sltr)
        self.goal.group_members.add('lotus')
        self.goal.run()
        installs = self.goal.list_installs()
        mrkite = [pkg for pkg in installs if pkg.name == 'mrkite'][0]
        lotus = [pkg for pkg in installs if pkg.name == 'lotus'][0]
        trampoline = [pkg for pkg in installs if pkg.name == 'trampoline'][0]
        self.assertEqual(self.goal.get_reason(lotus), libdnf.transaction.TransactionItemReason_GROUP)
        self.assertEqual(self.goal.get_reason(mrkite), libdnf.transaction.TransactionItemReason_USER)
        self.assertEqual(self.goal.get_reason(trampoline), libdnf.transaction.TransactionItemReason_DEPENDENCY)

    def test_group_reason(self):
        hole = self.sack.query().filter(name='hole')[0]
        self.goal.group_members.add('hole')
        self.assertEqual(libdnf.transaction.TransactionItemReason_GROUP, self.goal.group_reason(hole, libdnf.transaction.TransactionItemReason_GROUP))
        self.assertEqual(libdnf.transaction.TransactionItemReason_DEPENDENCY, self.goal.group_reason(hole, libdnf.transaction.TransactionItemReason_DEPENDENCY))
