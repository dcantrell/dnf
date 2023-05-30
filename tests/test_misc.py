# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import dnf.yum.misc

import tests.support


class TestGenericHolder(tests.support.TestCase):
    def test_merge_lists(self):
        gh = dnf.yum.misc.GenericHolder()
        gh2 = dnf.yum.misc.GenericHolder()
        gh.l = ["lucy", "in", "the"]
        gh2.l = ["sky"]
        gh2.l2 = ["with", "diamonds"]
        gh.merge_lists(gh2)
        self.assertEqual(gh.l, ["lucy", "in", "the", "sky"])
        self.assertEqual(gh.l2, ["with", "diamonds"])
