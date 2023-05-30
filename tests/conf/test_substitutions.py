# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import os

import dnf.conf

import tests.support


FN = tests.support.resource_path('etc/repos.conf')


class SubstitutionsFromEnvironmentTest(tests.support.TestCase):
    def test_numeric(self):
        env = os.environ
        os.environ['DNF0'] = 'the_zero'
        conf = dnf.conf.Conf()
        os.environ = env
        self.assertIn('DNF0', conf.substitutions)
        self.assertEqual('the_zero', conf.substitutions['DNF0'])

    def test_named(self):
        env = os.environ
        os.environ['DNF_VAR_GENRE'] = 'opera'
        os.environ['DNF_VAR_EMPTY'] = ''
        os.environ['DNF_VAR_MAL$FORMED'] = 'not this'
        os.environ['DNF_VARMALFORMED'] = 'not this'
        os.environ['DNF_VAR_MALFORMED '] = 'not this'
        conf = dnf.conf.Conf()
        os.environ = env
        self.assertCountEqual(
            conf.substitutions.keys(),
            ['basearch', 'arch', 'GENRE', 'EMPTY'])
        self.assertEqual('opera', conf.substitutions['GENRE'])
