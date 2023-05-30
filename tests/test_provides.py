# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import tests.support


class ProvidesTest(tests.support.DnfBaseTestCase):

    REPOS = ['main']

    def test_file(self):
        self.assertLength(self.base.provides("*ais*smile")[0], 1)
        self.assertLength(self.base.provides("/raised/smile")[0], 1)

    def test_name(self):
        self.assertLength(self.base.provides("henry(the_horse)")[0], 1)
        self.assertLength(self.base.provides("lotus")[0], 2)

    def test_glob(self):
        self.assertLength(self.base.provides("henry(*)")[0], 1)
        self.assertEqual(set(self.base.provides("dup*")[0]), set(self.base.provides('dup')[0]))
        self.assertEqual(set(self.base.provides(["dup*"])[0]), set(self.base.provides('dup')[0]))
