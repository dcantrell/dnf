# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import unicode_literals

import dnf.plugin


class DisabledPlugin(dnf.plugin.Plugin):

    name = 'disabled-plugin'
    config_name = 'disabled'
