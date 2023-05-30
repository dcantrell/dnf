#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
from dnf.i18n import _
from dnf.cli.commands.upgrade import UpgradeCommand


class UpgradeMinimalCommand(UpgradeCommand):
    """A class containing methods needed by the cli to execute the check
    command.
    """

    aliases = ('upgrade-minimal', 'update-minimal', 'up-min')
    summary = _("upgrade, but only 'newest' package match which fixes a problem"
                " that affects your system")

    def configure(self):
        UpgradeCommand.configure(self)

        self.upgrade_minimal = True
        if not any([self.opts.bugfix, self.opts.enhancement,
                   self.opts.newpackage, self.opts.security, self.opts.advisory,
                   self.opts.bugzilla, self.opts.cves, self.opts.severity]):
            self.all_security = True
