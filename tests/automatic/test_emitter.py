# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.automatic.emitter

import tests.support
from tests.support import mock, mock_open


MSG = """\
downloaded on myhost:
packages..."""


class TestEmitter(tests.support.TestCase):
    def test_prepare_msg(self):
        emitter = dnf.automatic.emitter.Emitter('myhost')
        emitter.notify_available('packages...')
        emitter.notify_downloaded()
        with mock.patch('dnf.automatic.emitter.DOWNLOADED', 'downloaded on %s:'):
            self.assertEqual(emitter._prepare_msg(), MSG)


class TestMotdEmitter(tests.support.TestCase):
    def test_motd(self):
        m = mock_open()
        with mock.patch('dnf.automatic.emitter.open', m, create=True):
            emitter = dnf.automatic.emitter.MotdEmitter('myhost')
            emitter.notify_available('packages...')
            emitter.notify_downloaded()
            with mock.patch('dnf.automatic.emitter.DOWNLOADED', 'downloaded on %s:'):
                emitter.commit()
            handle = m()
            handle.write.assert_called_once_with(MSG)
