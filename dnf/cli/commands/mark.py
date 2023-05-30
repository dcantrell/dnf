# mark.py
# Mark CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import print_function
from __future__ import unicode_literals

import libdnf.transaction

from dnf.i18n import _
from dnf.cli import commands

import dnf
import functools
import logging

logger = logging.getLogger("dnf")


class MarkCommand(commands.Command):

    aliases = ('mark',)
    summary = _('mark or unmark installed packages as installed by user.')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('mark', nargs=1, choices=['install', 'remove', 'group'],
                            help=_("install: mark as installed by user\n"
                                   "remove: unmark as installed by user\n"
                                   "group: mark as installed by group"))
        parser.add_argument('package', nargs='+', metavar="PACKAGE",
                            help=_("Package specification"))

    def _mark_install(self, pkg):
        self.base.history.set_reason(pkg, libdnf.transaction.TransactionItemReason_USER)
        logger.info(_('%s marked as user installed.'), str(pkg))

    def _mark_remove(self, pkg):
        self.base.history.set_reason(pkg, libdnf.transaction.TransactionItemReason_DEPENDENCY)
        logger.info(_('%s unmarked as user installed.'), str(pkg))

    def _mark_group(self, pkg):
        self.base.history.set_reason(pkg, libdnf.transaction.TransactionItemReason_GROUP)
        logger.info(_('%s marked as group installed.'), str(pkg))

    def configure(self):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.root_user = True
        demands.available_repos = False
        demands.resolving = False

    def run(self):
        cmd = self.opts.mark[0]
        pkgs = self.opts.package

        mark_func = functools.partial(getattr(self, '_mark_' + cmd))

        notfound = []
        for pkg in pkgs:
            subj = dnf.subject.Subject(pkg)
            q = subj.get_best_query(self.base.sack)
            for pkg in q:
                mark_func(pkg)
            if len(q) == 0:
                notfound.append(pkg)

        if notfound:
            logger.error(_('Error:'))
            for pkg in notfound:
                logger.error(_('Package %s is not installed.'), pkg)
            raise dnf.cli.CliError

        old = self.base.history.last()
        if old is None:
            rpmdb_version = self.base._ts.dbCookie()
        else:
            rpmdb_version = old.end_rpmdb_version

        self.base.history.beg(rpmdb_version, [], [])
        self.base.history.end(rpmdb_version)
