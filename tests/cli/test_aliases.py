# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.cli.aliases
import os

import tests.support

CONF = tests.support.resource_path('etc/aliases.d/aliases.conf')


class AliasesTest(tests.support.TestCase):

    def setUp(self):
        # Set DNF_ALIASES_DISABLED so that no default config is loaded
        self.env_var_set = False
        if 'DNF_ALIASES_DISABLED' not in os.environ:
            os.environ['DNF_ALIASES_DISABLED'] = '1'
            self.env_var_set = True

        self.aliases_base = dnf.cli.aliases.Aliases()
        self.aliases_base._load_aliases([CONF])

    def tearDown(self):
        if self.env_var_set:
            del os.environ['DNF_ALIASES_DISABLED']

    def test_undefined(self):
        args = ['undefined', 'undefined2']
        expected_args = list(args)
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_simple(self):
        args = ['h']
        expected_args = ['history']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_command_changed(self):
        args = ['cu']
        expected_args = ['check-update']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_package_unchanged(self):
        args = ['install', 'cu']
        expected_args = ['install', 'cu']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_recursive(self):
        args = ['lsi']
        expected_args = ['list', 'installed']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_options(self):
        args = ['FORCE']
        expected_args = ['--skip-broken', '--disableexcludes=all']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)

    def test_options_recursive(self):
        args = ['force-inst']
        expected_args = ['--skip-broken', '--disableexcludes=all', 'install']
        args = self.aliases_base._resolve(args)
        self.assertEqual(args, expected_args)
