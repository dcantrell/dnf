# reinstall.py
# Reinstall CLI command.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
from dnf.cli import commands
from dnf.cli.option_parser import OptionParser
from dnf.i18n import _

import dnf.exceptions
import logging

logger = logging.getLogger('dnf')


class ReinstallCommand(commands.Command):
    """A class containing methods needed by the cli to execute the reinstall command.
    """

    aliases = ('reinstall', 'rei')
    summary = _('reinstall a package')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('packages', nargs='+', help=_('Package to reinstall'),
                            action=OptionParser.ParseSpecGroupFileCallback,
                            metavar=_('PACKAGE'))

    def configure(self):
        """Verify that conditions are met so that this command can
        run.  These include that the program is being run by the root
        user, that there are enabled repositories with gpg keys, and
        that this command is called with appropriate arguments.
        """
        demands = self.cli.demands
        demands.sack_activation = True
        demands.available_repos = True
        demands.resolving = True
        demands.root_user = True
        commands._checkGPGKey(self.base, self.cli)
        if not self.opts.filenames:
            commands._checkEnabledRepo(self.base)

    def run(self):

        # Reinstall files.
        done = False
        for pkg in self.base.add_remote_rpms(self.opts.filenames, strict=False,
                                             progress=self.base.output.progress):
            try:
                self.base.package_reinstall(pkg)
            except dnf.exceptions.MarkingError:
                logger.info(_('No match for argument: %s'),
                            self.base.output.term.bold(pkg.location))
            else:
                done = True

        # Reinstall packages.
        for pkg_spec in self.opts.pkg_specs + ['@' + x for x in self.opts.grp_specs]:
            try:
                self.base.reinstall(pkg_spec)
            except dnf.exceptions.PackagesNotInstalledError as err:
                for pkg in err.packages:
                    logger.info(_('Package %s available, but not installed.'),
                                self.output.term.bold(pkg.name))
                    break
                logger.info(_('No match for argument: %s'),
                            self.base.output.term.bold(pkg_spec))
            except dnf.exceptions.PackagesNotAvailableError as err:
                for pkg in err.packages:
                    xmsg = ''
                    pkgrepo = self.base.history.repo(pkg)
                    if pkgrepo:
                        xmsg = _(' (from %s)') % pkgrepo
                    msg = _('Installed package %s%s not available.')
                    logger.info(msg, self.base.output.term.bold(pkg),
                                xmsg)
            except dnf.exceptions.MarkingError:
                assert False, 'Only the above marking errors are expected.'
            else:
                done = True

        if not done:
            raise dnf.exceptions.Error(_('No packages marked for reinstall.'))
