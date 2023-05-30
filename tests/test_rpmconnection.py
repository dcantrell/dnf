# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import inspect

from dnf.rpm.connection import RpmConnection

import tests.support


class TestConnection(tests.support.TestCase):
    def test_sanity(self):
        rpm = RpmConnection('/')
        ts = rpm.readonly_ts
        self.assertTrue(inspect.isbuiltin(ts.clean))
