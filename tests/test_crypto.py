# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import os
import tempfile

import dnf.crypto
import dnf.util
import dnf.yum.misc

import tests.support


FINGERPRINT = '0BE49FAF9C955F4F1A98D14B24362A8492530C8E'
KEYFILE = tests.support.resource_path('keys/key.pub')
KEYFILE_URL = 'file://%s' % KEYFILE


class CryptoTest(tests.support.TestCase):
    PUBRING_DIR = None

    @classmethod
    def setUpClass(cls):
        cls.PUBRING_DIR = tempfile.mkdtemp()
        with open(KEYFILE, 'rb') as keyfile:
            keyinfo = dnf.crypto.rawkey2infos(keyfile)[0]
        dnf.yum.misc.import_key_to_pubring(
            keyinfo.raw_key, keyinfo.short_id, gpgdir=cls.PUBRING_DIR,
            make_ro_copy=False)

    @classmethod
    def tearDownClass(cls):
        dnf.util.rm_rf(cls.PUBRING_DIR)

    def test_keyids_from_pubring(self):
        ids = dnf.crypto.keyids_from_pubring(self.PUBRING_DIR)
        self.assertIn('24362A8492530C8E', ids)

    def test_printable_fingerprint(self):
        self.assertEqual(dnf.crypto._printable_fingerprint(FINGERPRINT),
                         '0BE4 9FAF 9C95 5F4F 1A98 D14B 2436 2A84 9253 0C8E')

    def test_pubring_dir(self):
        self.assertNotEqual(os.environ.get('GNUPGHOME'), self.PUBRING_DIR)
        with dnf.crypto.pubring_dir(self.PUBRING_DIR):
            self.assertEqual(os.environ['GNUPGHOME'], self.PUBRING_DIR)

    def test_rawkey2infos(self):
        with open(KEYFILE, 'rb') as keyfile:
            info = dnf.crypto.rawkey2infos(keyfile)[0]
        self.assertEqual(info.fingerprint, FINGERPRINT)
        self.assertEqual(info.short_id, '92530C8E')
        self.assertEqual(info.rpm_id, '92530c8e')
        self.assertIn(b'Frmy6HXUL\n', info.raw_key)
        self.assertEqual(info.timestamp, 1408534646)
        self.assertEqual(info.userid, 'Dandy Fied <dnf@example.com>')

    def test_retrieve(self):
        keyinfos = dnf.crypto.retrieve(KEYFILE_URL)
        self.assertLength(keyinfos, 1)
        keyinfo = keyinfos[0]
        self.assertEqual(keyinfo.url, KEYFILE_URL)
