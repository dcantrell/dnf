# downgrade.py
# Downgrade CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
from dnf.cli import commands
from dnf.cli.option_parser import OptionParser
from dnf.i18n import _


class DowngradeCommand(commands.Command):
    """A class containing methods needed by the cli to execute the
    downgrade command.
    """

    aliases = ('downgrade', 'dg')
    summary = _("Downgrade a package")

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('package', nargs='*', help=_('Package to downgrade'),
                            action=OptionParser.ParseSpecGroupFileCallback)

    def configure(self):
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.resolving = True
        demands.root_user = True

        commands._checkGPGKey(self.base, self.cli)
        if not self.opts.filenames:
            commands._checkEnabledRepo(self.base)

    def run(self):
        file_pkgs = self.base.add_remote_rpms(self.opts.filenames, strict=False,
                                              progress=self.base.output.progress)
        return self.base.downgradePkgs(
            specs=self.opts.pkg_specs + ['@' + x for x in self.opts.grp_specs],
            file_pkgs=file_pkgs,
            strict=self.base.conf.strict)
