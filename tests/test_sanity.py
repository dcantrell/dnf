# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import sys

import tests.support


class Sanity(tests.support.TestCase):
    def test_sanity(self):
        assert(os.access(tests.support.repo("@System.repo"), os.R_OK))
        sack = tests.support.mock_sack()
        assert(sack)
        self.assertEqual(len(sack), tests.support.SYSTEM_NSOLVABLES)

        sack2 = tests.support.MockBase("main", "updates").sack
        self.assertEqual(len(sack2), tests.support.TOTAL_NSOLVABLES)

    def test_toplevel(self):
        self.assertIn(tests.support.dnf_toplevel(), sys.path)
