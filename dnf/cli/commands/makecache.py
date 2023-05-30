# makecache.py
# Makecache CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
from dnf.cli import commands
from dnf.i18n import _

import argparse
import dnf.cli
import dnf.exceptions
import dnf.util
import logging

logger = logging.getLogger("dnf")


class MakeCacheCommand(commands.Command):
    aliases = ('makecache', 'mc')
    summary = _('generate the metadata cache')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('--timer', action='store_true', dest="timer_opt")
        # compatibility with dnf < 2.0
        parser.add_argument('timer', nargs='?', choices=['timer'],
                            metavar='timer', help=argparse.SUPPRESS)

    def run(self):
        timer = self.opts.timer is not None or self.opts.timer_opt
        msg = _("Making cache files for all metadata files.")
        logger.debug(msg)
        return self.base.update_cache(timer)
