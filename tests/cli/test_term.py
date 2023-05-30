# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import io

import dnf.cli.term

import tests.support
from tests.support import mock


class TermTest(tests.support.TestCase):

    """Tests of ```dnf.cli.term.Term``` class."""

    def test_mode_tty(self):
        """Test whether all modes are properly set if the stream is a tty.

        It also ensures that all the values are unicode strings.

        """
        tty = mock.create_autospec(io.IOBase)
        tty.isatty.return_value = True

        def tigetstr(name):
            return '<cap_%(name)s>' % locals()

        with mock.patch('curses.tigetstr', autospec=True, side_effect=tigetstr):
            term = dnf.cli.term.Term(tty)

        self.assertEqual(term.MODE,
                         {u'blink': tigetstr(u'blink'),
                          u'bold': tigetstr(u'bold'),
                          u'dim': tigetstr(u'dim'),
                          u'normal': tigetstr(u'sgr0'),
                          u'reverse': tigetstr(u'rev'),
                          u'underline': tigetstr(u'smul')})

    def test_mode_tty_incapable(self):
        """Test whether modes correct if the stream is an incapable tty.

        It also ensures that all the values are unicode strings.

        """
        tty = mock.create_autospec(io.IOBase)
        tty.isatty.return_value = True

        with mock.patch('curses.tigetstr', autospec=True, return_value=None):
            term = dnf.cli.term.Term(tty)

        self.assertEqual(term.MODE,
                         {u'blink': u'',
                          u'bold': u'',
                          u'dim': u'',
                          u'normal': u'',
                          u'reverse': u'',
                          u'underline': u''})

    def test_mode_nontty(self):
        """Test whether all modes are properly set if the stream is not a tty.

        It also ensures that all the values are unicode strings.

        """
        nontty = mock.create_autospec(io.IOBase)
        nontty.isatty.return_value = False

        term = dnf.cli.term.Term(nontty)

        self.assertEqual(term.MODE,
                         {u'blink': u'',
                          u'bold': u'',
                          u'dim': u'',
                          u'normal': u'',
                          u'reverse': u'',
                          u'underline': u''})
