# autoremove.py
# Autoremove CLI command.
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
import hawkey
import logging

logger = logging.getLogger("dnf")


class AutoremoveCommand(commands.Command):

    nevra_forms = {'autoremove-n': hawkey.FORM_NAME,
                   'autoremove-na': hawkey.FORM_NA,
                   'autoremove-nevra': hawkey.FORM_NEVRA}

    aliases = ('autoremove',) + tuple(nevra_forms.keys())
    summary = _('remove all unneeded packages that were originally installed '
                'as dependencies')

    @staticmethod
    def set_argparser(parser):
        parser.add_argument('packages', nargs='*', help=_('Package to remove'),
                            action=OptionParser.ParseSpecGroupFileCallback,
                            metavar=_('PACKAGE'))

    def configure(self):
        demands = self.cli.demands
        demands.resolving = True
        demands.root_user = True
        demands.sack_activation = True

        if any([self.opts.grp_specs, self.opts.pkg_specs, self.opts.filenames]):
            self.base.conf.clean_requirements_on_remove = True
            demands.allow_erasing = True
            # disable all available repos to delete whole dependency tree
            # instead of replacing removable package with available packages
            demands.available_repos = False
        else:
            demands.available_repos = True
            demands.fresh_metadata = False

    def run(self):
        if any([self.opts.grp_specs, self.opts.pkg_specs, self.opts.filenames]):
            forms = []
            if self.opts.command in self.nevra_forms:
                forms = [self.nevra_forms[self.opts.command]]

            self.base.autoremove(forms,
                                 self.opts.pkg_specs,
                                 self.opts.grp_specs,
                                 self.opts.filenames)
        else:
            self.base.autoremove()
