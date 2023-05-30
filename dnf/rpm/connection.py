# connection.py
# Maintain RPMDB connections.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals

from .transaction import initReadOnlyTransaction
import dnf.util

class RpmConnection(object):
    def __init__(self, root):
        self.root = root

    @property
    @dnf.util.lazyattr("_readonly_ts")
    def readonly_ts(self):
        return initReadOnlyTransaction(self.root)
