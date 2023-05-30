# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

"""Unit test dnf.lock module.

Locking is very hard to cover reasonably with a unit test, this is more or less
just a sanity check.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import multiprocessing
import os
import re
import threading


import dnf.lock
import dnf.pycomp
import dnf.util
from dnf.exceptions import ProcessLockError, ThreadLockError

import tests.support
from tests.support import mock


class ConcurrencyMixin(object):
    def __init__(self, lock):
        self.lock = lock

    def run(self):
        try:
            with self.lock:
                pass
        except (ProcessLockError, ThreadLockError) as e:
            self.queue.put(e)


class OtherThread(ConcurrencyMixin, threading.Thread):
    def __init__(self, lock):
        ConcurrencyMixin.__init__(self, lock)
        threading.Thread.__init__(self)
        self.queue = dnf.pycomp.Queue(1)


class OtherProcess(ConcurrencyMixin, multiprocessing.Process):
    def __init__(self, lock):
        ConcurrencyMixin.__init__(self, lock)
        multiprocessing.Process.__init__(self)
        self.queue = multiprocessing.Queue(1)


TARGET = os.path.join(tests.support.USER_RUNDIR, 'unit-test.pid')


def build_lock(blocking=False):
    return dnf.lock.ProcessLock(TARGET, 'unit-tests', blocking)


class LockTest(tests.support.TestCase):
    def test_fit_lock_dir(self):
        orig = '/some'
        with mock.patch('dnf.util.am_i_root', return_value=True):
            self.assertEqual(dnf.lock._fit_lock_dir(orig), '/some')
        with mock.patch('dnf.util.am_i_root', return_value=False):
            dir_ = dnf.lock._fit_lock_dir(orig)
            match = re.match(
                r'/var/tmp/dnf-[^:]+-[^/]+/locks/2690814ff0269c86e5109d2915ea572092918cb3',
                dir_)
            self.assertTrue(match)


class ProcessLockTest(tests.support.TestCase):
    @classmethod
    def tearDownClass(cls):
        dnf.util.rm_rf(tests.support.USER_RUNDIR)

    def test_simple(self):
        l1 = build_lock()
        target = l1.target
        with l1:
            self.assertFile(target)
        self.assertPathDoesNotExist(target)

    def test_reentrance(self):
        l1 = build_lock()
        with l1:
            with l1:
                pass

    def test_another_process(self):
        l1 = build_lock()
        process = OtherProcess(l1)
        with l1:
            process.start()
            process.join()
        self.assertIsInstance(process.queue.get(), ProcessLockError)

    def test_another_process_blocking(self):
        l1 = build_lock(blocking=True)
        l2 = build_lock(blocking=True)
        process = OtherProcess(l1)
        target = l1.target
        with l2:
            process.start()
        process.join()
        self.assertEqual(process.queue.empty(), True)
        self.assertPathDoesNotExist(target)

    def test_another_thread(self):
        l1 = build_lock()
        thread = OtherThread(l1)
        with l1:
            thread.start()
            thread.join()
        self.assertIsInstance(thread.queue.get(), ThreadLockError)
