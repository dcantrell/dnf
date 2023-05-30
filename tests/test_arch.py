# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.rpm

import tests.support


class ArchTest(tests.support.TestCase):

    def test_basearch(self):
        fn = dnf.rpm.basearch
        self.assertEqual(fn('armv6hl'), 'armhfp')
        self.assertEqual(fn('armv7hl'), 'armhfp')
        self.assertEqual(fn('armv8hl'), 'armhfp')
        self.assertEqual(fn('armv8l'), 'arm')
        self.assertEqual(fn('i686'), 'i386')
        self.assertEqual(fn('noarch'), 'noarch')
        self.assertEqual(fn('ppc64iseries'), 'ppc64')
        self.assertEqual(fn('sparc64v'), 'sparc')
        self.assertEqual(fn('x86_64'), 'x86_64')
