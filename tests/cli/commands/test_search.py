# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

import dnf.cli.commands.search as search
import dnf.match_counter
import dnf.pycomp

import tests.support
from tests import mock


class SearchCountedTest(tests.support.DnfBaseTestCase):

    REPOS = ["main"]
    CLI = "mock"

    def setUp(self):
        super(SearchCountedTest, self).setUp()
        self.cmd = search.SearchCommand(self.cli)

    def test_search_counted(self):
        counter = dnf.match_counter.MatchCounter()
        self.cmd._search_counted(counter, 'summary', 'ation')
        self.assertEqual(len(counter), 2)
        haystacks = set()
        for pkg in counter:
            haystacks.update(counter.matched_haystacks(pkg))
        self.assertCountEqual(haystacks, ["It's an invitation.",
                                          "Make a reservation."])

    def test_search_counted_glob(self):
        counter = dnf.match_counter.MatchCounter()
        self.cmd._search_counted(counter, 'summary', '*invit*')
        self.assertEqual(len(counter), 1)


class SearchTest(tests.support.DnfBaseTestCase):

    REPOS = ["search"]
    CLI = "mock"

    def setUp(self):
        super(SearchTest, self).setUp()
        self.base.output = mock.MagicMock()
        self.base.output.fmtSection = lambda str: str
        self.cmd = search.SearchCommand(self.cli)

    def patched_search(self, *args):
        with tests.support.patch_std_streams() as (stdout, _):
            tests.support.command_run(self.cmd, *args)
            call_args = self.base.output.matchcallback.call_args_list
            pkgs = [c[0][0] for c in call_args]
            return (stdout.getvalue(), pkgs)

    def test_search(self):
        (_, pkgs) = self.patched_search(['lotus'])
        pkg_names = list(map(str, pkgs))
        self.assertIn('lotus-3-16.i686', pkg_names)
        self.assertIn('lotus-3-16.x86_64', pkg_names)

    @mock.patch('dnf.cli.commands.search._',
                dnf.pycomp.NullTranslations().ugettext)
    def test_search_caseness(self):
        (stdout, pkgs) = self.patched_search(['LOTUS'])
        self.assertEqual(stdout, 'Name Matched: LOTUS\n')
        pkg_names = map(str, pkgs)
        self.assertIn('lotus-3-16.i686', pkg_names)
        self.assertIn('lotus-3-16.x86_64', pkg_names)
