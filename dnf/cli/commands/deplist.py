#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from dnf.i18n import _
from dnf.cli.commands.repoquery import RepoQueryCommand


class DeplistCommand(RepoQueryCommand):
    """
    The command is alias for 'dnf repoquery --deplist'
    """

    aliases = ('deplist',)
    summary = _("[deprecated, use repoquery --deplist] List package's dependencies and what packages provide them")

    def configure(self):
        RepoQueryCommand.configure(self)
        self.opts.deplist = True
