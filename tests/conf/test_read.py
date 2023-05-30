# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.conf
import dnf.conf.read

import tests.support


FN = tests.support.resource_path('etc/repos.conf')


class RepoReaderTest(tests.support.TestCase):
    def test_read(self):
        conf = dnf.conf.Conf()
        conf.config_file_path = FN
        conf.reposdir = []
        reader = dnf.conf.read.RepoReader(conf, {})
        all_repos = list(reader)
        self.assertLength(all_repos, 2)

        r1 = all_repos[0]
        self.assertEqual(r1.id, 'fixing')
        self.assertEqual(r1.baseurl, ['http://cracks'])

        r2 = all_repos[1]
        self.assertEqual(r2.id, 'rain')
        self.assertEqual(r2.mirrorlist, 'http://through.net')
