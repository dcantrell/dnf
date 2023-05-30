# upgrade.py
# Upgrade CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals

import logging

import dnf.exceptions
import dnf.base
from dnf.cli import commands
from dnf.cli.option_parser import OptionParser
from dnf.i18n import _

logger = logging.getLogger('dnf')


class UpgradeCommand(commands.Command):
    """A class containing methods needed by the cli to execute the
    update command.
    """
    aliases = ('upgrade', 'update', 'upgrade-to', 'update-to', 'localupdate', 'up')
    summary = _('upgrade a package or packages on your system')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('packages', nargs='*', help=_('Package to upgrade'),
                            action=OptionParser.ParseSpecGroupFileCallback,
                            metavar=_('PACKAGE'))

    def configure(self):
        """Verify that conditions are met so that this command can run.

        These include that there are enabled repositories with gpg
        keys, and that this command is being run by the root user.
        """
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.resolving = True
        demands.root_user = True
        commands._checkGPGKey(self.base, self.cli)
        if not self.opts.filenames:
            commands._checkEnabledRepo(self.base)
        self.upgrade_minimal = None
        self.all_security = None
        self.skipped_grp_specs = None

    def run(self):
        cmp_type = "eq" if self.upgrade_minimal else "gte"
        self.cli._populate_update_security_filter(self.opts, cmp_type=cmp_type,
                                                  all=self.all_security)

        if self.opts.filenames or self.opts.pkg_specs or self.opts.grp_specs:
            result = False
            result |= self._update_modules()
            result |= self._update_files()
            result |= self._update_packages()
            result |= self._update_groups()

            if result:
                return
        else:
            self.base.upgrade_all()
            return

        raise dnf.exceptions.Error(_('No packages marked for upgrade.'))

    def _update_modules(self):
        group_specs_num = len(self.opts.grp_specs)
        if dnf.base.WITH_MODULES:
            module_base = dnf.module.module_base.ModuleBase(self.base)
            self.skipped_grp_specs = module_base.upgrade(self.opts.grp_specs)
        else:
            self.skipped_grp_specs = self.opts.grp_specs

        return len(self.skipped_grp_specs) != group_specs_num

    def _update_files(self):
        success = False
        if self.opts.filenames:
            for pkg in self.base.add_remote_rpms(self.opts.filenames, strict=False,
                                                 progress=self.base.output.progress):
                try:
                    self.base.package_upgrade(pkg)
                    success = True
                except dnf.exceptions.MarkingError as e:
                    logger.info(_('No match for argument: %s'),
                                self.base.output.term.bold(pkg.location))
        return success

    def _update_packages(self):
        success = False
        for pkg_spec in self.opts.pkg_specs:
            try:
                self.base.upgrade(pkg_spec)
                success = True
            except dnf.exceptions.MarkingError as e:
                logger.info(_('No match for argument: %s'),
                            self.base.output.term.bold(pkg_spec))
        return success

    def _update_groups(self):
        if self.skipped_grp_specs:
            self.base.env_group_upgrade(self.skipped_grp_specs)
            return True
        return False
