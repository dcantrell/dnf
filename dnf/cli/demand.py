# demand.py
# Demand sheet and related classes.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import unicode_literals


class _BoolDefault(object):
    def __init__(self, default):
        self.default = default
        self._storing_name = '__%s%x' % (self.__class__.__name__, id(self))

    def __get__(self, obj, objtype=None):
        objdict = obj.__dict__
        if self._storing_name in objdict:
            return objdict[self._storing_name]
        return self.default

    def __set__(self, obj, val):
        objdict = obj.__dict__
        if self._storing_name in objdict:
            current_val = objdict[self._storing_name]
            if current_val != val:
                raise AttributeError('Demand already set.')
        objdict[self._storing_name] = val

class DemandSheet(object):
    """Collection of demands that different CLI parts have on other parts. :api"""

    # :api...
    allow_erasing = _BoolDefault(False)
    available_repos = _BoolDefault(False)
    resolving = _BoolDefault(False)
    root_user = _BoolDefault(False)
    sack_activation = _BoolDefault(False)
    load_system_repo = _BoolDefault(True)
    success_exit_status = 0

    cacheonly = _BoolDefault(False)
    fresh_metadata = _BoolDefault(True)
    freshest_metadata = _BoolDefault(False)
    changelogs = _BoolDefault(False)

    transaction_display = None

    # This demand controlls applicability of the plugins that could filter
    # repositories packages (e.g. versionlock).
    # If it stays None, the demands.resolving is used as a fallback.
    plugin_filtering_enabled = _BoolDefault(None)
