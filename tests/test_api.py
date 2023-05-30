# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import dnf
from dnf.pycomp import unicode

import tests.support


class APITest(tests.support.TestCase):
    def test_base(self):
        self.assertIsInstance(dnf.Base, type)

    def test_conf(self):
        base = tests.support.MockBase()
        self.assertIsInstance(base.conf.installroot, unicode)
        # reasonable default
        self.assertEqual(base.conf.installroot, '/tmp/dnf-test-installroot/')
        # assignable
        dnf.conf.installroot = '/mnt/rootimage'
