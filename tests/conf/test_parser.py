# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.conf
from libdnf.conf import ConfigParser

import tests.support

substitute = ConfigParser.substitute


class ParserTest(tests.support.TestCase):
    def test_substitute(self):
        substs = {'lies': 'fact'}
        # Test a single word without braces
        rawstr = '$Substitute some $lies.'
        result = '$Substitute some fact.'
        self.assertEqual(substitute(rawstr, substs), result)
        # And with braces
        rawstr = '$Substitute some ${lies}.'
        self.assertEqual(substitute(rawstr, substs), result)

        # Test a word with braces without space
        rawstr = '$Substitute some ${lies}withoutspace.'
        result = '$Substitute some factwithoutspace.'
        self.assertEqual(substitute(rawstr, substs), result)

        # Tests a single brace before (no substitution)
        rawstr = '$Substitute some ${lieswithoutspace.'
        result = '$Substitute some ${lieswithoutspace.'
        self.assertEqual(substitute(rawstr, substs), result)

        # Tests a single brace after (substitution and leave the brace)
        rawstr = '$Substitute some $lies}withoutspace.'
        result = '$Substitute some fact}withoutspace.'
        self.assertEqual(substitute(rawstr, substs), result)

    def test_empty_option(self):
        # Parser is able to read config file with option without value
        FN = tests.support.resource_path('etc/empty_option.conf')
        conf = dnf.conf.Conf()
        conf.config_file_path = FN
        conf.read()
        self.assertEqual(conf.reposdir, '')
