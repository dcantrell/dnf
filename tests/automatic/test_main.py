# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.automatic.main

import tests.support


FILE = tests.support.resource_path('etc/automatic.conf')


class TestConfig(tests.support.TestCase):
    def test_load(self):
        # test values from config file take effect if no overrides
        # note: config file specifies download = no apply = yes,
        # test expects implication to turn download into True
        conf = dnf.automatic.main.AutomaticConfig(FILE)
        self.assertTrue(conf.commands.apply_updates)
        self.assertTrue(conf.commands.download_updates)
        self.assertEqual(conf.commands.random_sleep, 300)
        self.assertEqual(conf.email.email_from, 'staring@crowd.net')

        # test overriding installupdates
        conf = dnf.automatic.main.AutomaticConfig(FILE, installupdates=False)
        # as per above, download is set false in config
        self.assertFalse(conf.commands.download_updates)
        self.assertFalse(conf.commands.apply_updates)

        # test overriding installupdates and downloadupdates
        conf = dnf.automatic.main.AutomaticConfig(FILE, downloadupdates=True, installupdates=False)
        self.assertTrue(conf.commands.download_updates)
        self.assertFalse(conf.commands.apply_updates)

        # test that reboot is "never" by default
        conf = dnf.automatic.main.AutomaticConfig(FILE)
        self.assertEqual(conf.commands.reboot, 'never')
