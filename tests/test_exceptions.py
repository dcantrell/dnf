# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.exceptions

import tests.support


JAY_ERR = """jay-3.x86_64: Can not download."""


class DownloadErrorTest(tests.support.TestCase):

    def test_str(self):
        exc = dnf.exceptions.DownloadError(errmap={
            'jay-3.x86_64': ['Can not download.']})
        self.assertEqual(str(exc), JAY_ERR)

        exc = dnf.exceptions.DownloadError(errmap={'': ['Epic fatal.']})
        self.assertEqual(str(exc), 'Epic fatal.')
