# distrosync.py
# distro-sync CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from dnf.cli import commands
from dnf.i18n import _


class DistroSyncCommand(commands.Command):
    """A class containing methods needed by the cli to execute the
    distro-synch command.
    """

    aliases = ('distro-sync', 'distrosync', 'distribution-synchronization', 'dsync')
    summary = _('synchronize installed packages to the latest available versions')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('package', nargs='*', help=_('Package to synchronize'))

    def configure(self):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.resolving = True
        demands.root_user = True
        commands._checkGPGKey(self.base, self.cli)
        commands._checkEnabledRepo(self.base, self.opts.package)

    def run(self):
        return self.base.distro_sync_userlist(self.opts.package)
