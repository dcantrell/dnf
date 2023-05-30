# __init__.py
# DNF cli subpackage.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
import dnf.exceptions


class CliError(dnf.exceptions.Error):
    """CLI Exception. :api"""
    pass


from dnf.cli.cli import Cli  # :api
from dnf.cli.commands import Command  # :api
