# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

"""Tests of the CLI entry point."""

from __future__ import unicode_literals

import dnf.cli.main
import dnf.logging
import dnf.pycomp

import tests.support


class MainTest(tests.support.TestCase):
    """Tests the ``dnf.cli.main`` module."""

    def test_ex_IOError_logs_traceback(self):
        """Test whether the traceback is logged if an error is raised."""

        lvl = dnf.logging.SUBDEBUG
        out = dnf.pycomp.StringIO()

        with tests.support.wiretap_logs('dnf', lvl, out):
            try:
                raise OSError('test_ex_IOError_logs_traceback')
            except OSError as e:
                dnf.cli.main.ex_IOError(e)
        self.assertTracebackIn('OSError: test_ex_IOError_logs_traceback\n',
                               out.getvalue())
