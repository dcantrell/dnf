# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import dnf.plugin


class LuckyPlugin(dnf.plugin.Plugin):

    name = 'lucky'

    def __init__(self, *args):
        self._config = False

    def config(self):
        self._config = True
