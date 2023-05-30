# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import dnf.repodict

import tests.support
from tests.support import TestCase


class TestRepoDict(TestCase):
    def setUp(self):
        conf = tests.support.FakeConf()
        self.x = tests.support.MockRepo('x', conf)
        self.xx = tests.support.MockRepo('xx', conf)
        self.y = tests.support.MockRepo('y', conf)
        self.z = tests.support.MockRepo('z', conf)

        self.repos = dnf.repodict.RepoDict()
        self.repos.add(self.x)
        self.repos.add(self.xx)
        self.repos.add(self.y)
        self.repos.add(self.z)
        self.full_set = {self.x, self.xx, self.y, self.z}

    def test_any_enabled(self):
        self.assertTrue(self.repos._any_enabled())
        self.repos.get_matching("*").disable()
        self.assertFalse(self.repos._any_enabled())

    def test_get_matching(self):
        self.assertEqual(self.repos['x'], self.x)
        self.assertCountEqual(self.repos.get_matching('*'), self.full_set)
        self.assertCountEqual(self.repos.get_matching('y'), {self.y})
        self.assertCountEqual(self.repos.get_matching('x*'), {self.x, self.xx})

        self.assertCountEqual(self.repos.get_matching('nope'), [])

    def test_iter_enabled(self):
        self.assertCountEqual(self.repos.iter_enabled(), self.full_set)
        self.repos.get_matching('x*').disable()
        self.assertCountEqual(self.repos.iter_enabled(), {self.y, self.z})

    def test_all(self):
        self.assertCountEqual(self.repos.all(), self.full_set)
