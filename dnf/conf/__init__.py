# conf.py
# dnf configuration classes.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#


"""
The configuration classes and routines in yum are splattered over too many
places, hard to change and debug. The new structure here will replace that. Its
goal is to:

* accept configuration options from all three sources (the main config file,
  repo config files, command line switches)
* handle all the logic of storing those and producing related values.
* returning configuration values.
* optionally: asserting no value is overridden once it has been applied
  somewhere (e.g. do not let a new repo be initialized with different global
  cache path than an already existing one).

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from dnf.conf.config import PRIO_DEFAULT, PRIO_MAINCONFIG, PRIO_AUTOMATICCONFIG
from dnf.conf.config import PRIO_REPOCONFIG, PRIO_PLUGINDEFAULT, PRIO_PLUGINCONFIG
from dnf.conf.config import PRIO_COMMANDLINE, PRIO_RUNTIME

from dnf.conf.config import BaseConfig, MainConf, RepoConf

Conf = MainConf
