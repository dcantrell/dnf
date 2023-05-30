# __init__.py
# The toplevel DNF package.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import unicode_literals
import warnings
import dnf.pycomp

warnings.filterwarnings('once', category=DeprecationWarning, module=r'^dnf\..*$')

from dnf.const import VERSION
__version__ = VERSION  # :api

import dnf.base
Base = dnf.base.Base # :api

import dnf.plugin
Plugin = dnf.plugin.Plugin # :api

# setup libraries
dnf.pycomp.urlparse.uses_fragment.append("media")
