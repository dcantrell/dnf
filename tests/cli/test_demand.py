# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.cli.demand

import tests.support


class DemandTest(tests.support.TestCase):

    def test_bool_default(self):
        demands = dnf.cli.demand.DemandSheet()
        demands.resolving = True
        self.assertTrue(demands.resolving)
        demands.resolving = True
        self.assertTrue(demands.resolving)
        with self.assertRaises(AttributeError):
            demands.resolving = False

    def test_default(self):
        demands = dnf.cli.demand.DemandSheet()
        self.assertFalse(demands.resolving)
        self.assertFalse(demands.sack_activation)
        self.assertFalse(demands.root_user)
        self.assertEqual(demands.success_exit_status, 0)

    def test_independence(self):
        d1 = dnf.cli.demand.DemandSheet()
        d1.resolving = True
        d2 = dnf.cli.demand.DemandSheet()
        self.assertTrue(d1.resolving)
        self.assertFalse(d2.resolving)
