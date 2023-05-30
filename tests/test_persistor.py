# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import tempfile

import dnf.comps
import dnf.persistor
import dnf.pycomp

import tests.support


IDS = set(['one', 'two', 'three'])


class RepoPersistorTest(tests.support.TestCase):
    def setUp(self):
        self.persistdir = tempfile.mkdtemp(prefix="dnf-persistor-test-")
        self.persistor = dnf.persistor.RepoPersistor(self.persistdir)

    def tearDown(self):
        dnf.util.rm_rf(self.persistdir)

    def test_expired_repos(self):
        self.assertLength(self.persistor.get_expired_repos(), 0)
        self.persistor.expired_to_add = IDS
        self.persistor.save()
        self.assertEqual(self.persistor.get_expired_repos(), IDS)

        persistor = dnf.persistor.RepoPersistor(self.persistdir)
        self.assertEqual(persistor.get_expired_repos(), IDS)
