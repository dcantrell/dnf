# substitutions.py
# Config file substitutions.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

import logging
import os
import re

from dnf.i18n import _

ENVIRONMENT_VARS_RE = re.compile(r'^DNF_VAR_[A-Za-z0-9_]+$')
logger = logging.getLogger('dnf')


class Substitutions(dict):
    # :api

    def __init__(self):
        super(Substitutions, self).__init__()
        self._update_from_env()

    def _update_from_env(self):
        numericvars = ['DNF%d' % num for num in range(0, 10)]
        for key, val in os.environ.items():
            if ENVIRONMENT_VARS_RE.match(key):
                self[key[8:]] = val  # remove "DNF_VAR_" prefix
            elif key in numericvars:
                self[key] = val

    def update_from_etc(self, installroot, varsdir=("/etc/yum/vars/", "/etc/dnf/vars/")):
        # :api

        for vars_path in varsdir:
            fsvars = []
            try:
                dir_fsvars = os.path.join(installroot, vars_path.lstrip('/'))
                fsvars = os.listdir(dir_fsvars)
            except OSError:
                continue
            for fsvar in fsvars:
                filepath = os.path.join(dir_fsvars, fsvar)
                val = None
                if os.path.isfile(filepath):
                    try:
                        with open(filepath) as fp:
                            val = fp.readline()
                        if val and val[-1] == '\n':
                            val = val[:-1]
                    except (OSError, IOError, UnicodeDecodeError) as e:
                        logger.warning(_("Error when parsing a variable from file '{0}': {1}").format(filepath, e))
                        continue
                if val is not None:
                    self[fsvar] = val
