# query.py
# Implements Query.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
import hawkey

from hawkey import Query
from dnf.i18n import ucd
from dnf.pycomp import basestring



def _by_provides(sack, patterns, ignore_case=False, get_query=False):
    if isinstance(patterns, basestring):
        patterns = [patterns]

    q = sack.query()
    flags = []
    if ignore_case:
        flags.append(hawkey.ICASE)

    q.filterm(*flags, provides__glob=patterns)
    if get_query:
        return q
    return q.run()

def _per_nevra_dict(pkg_list):
    return {ucd(pkg):pkg for pkg in pkg_list}
