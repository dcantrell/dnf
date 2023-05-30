# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.exceptions

import tests.support


class SubjectTest(tests.support.DnfBaseTestCase):

    REPOS = ['main', 'third_party']

    def setUp(self):
        super(SubjectTest, self).setUp()
        pkg = self.base.sack.query().filter(name='lotus', arch='x86_64')[0]
        self.base.sack.add_excludes([pkg])

    def test_best_selectors_no_glob(self):
        subj = dnf.subject.Subject('pepper')
        sltrs = subj._get_best_selectors(self.base)
        self.assertEqual(len(sltrs), 1)

    def test_best_selectors_glob(self):
        subj = dnf.subject.Subject('l*')
        sltrs = subj._get_best_selectors(self.base)
        q = self.base.sack.query().filter(name__glob='l*')
        self.assertEqual(len(sltrs), len(set(map(lambda p: p.name, q))))

    def test_best_selectors_arch(self):
        subj = dnf.subject.Subject('l*.x86_64')
        sltrs = subj._get_best_selectors(self.base)
        q = self.base.sack.query().filter(name__glob='l*', arch__eq='x86_64')
        self.assertEqual(len(sltrs), len(set(map(lambda p: p.name, q))))
        for sltr in sltrs:
            for pkg in sltr.matches():
                self.assertEqual(pkg.arch, 'x86_64')

    def test_best_selectors_ver(self):
        subj = dnf.subject.Subject('*-1-1')
        sltrs = subj._get_best_selectors(self.base)
        for sltr in sltrs:
            for pkg in sltr.matches():
                self.assertEqual(pkg.evr, '1-1')
