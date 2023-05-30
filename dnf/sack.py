# sack.py
# The dnf.Sack class, derived from hawkey.Sack
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import unicode_literals
import dnf.util
import dnf.package
import dnf.query
import logging
import hawkey
import os
from dnf.pycomp import basestring
from dnf.i18n import _

logger = logging.getLogger("dnf")

class Sack(hawkey.Sack):
    # :api

    def __init__(self, *args, **kwargs):
        super(Sack, self).__init__(*args, **kwargs)

    def _configure(self, installonly=None, installonly_limit=0, allow_vendor_change=None):
        if installonly:
            self.installonly = installonly
        self.installonly_limit = installonly_limit
        if allow_vendor_change is not None:
            self.allow_vendor_change = allow_vendor_change
            if allow_vendor_change is False:
                logger.warning(_("allow_vendor_change is disabled. This option is currently not supported for downgrade and distro-sync commands"))

    def query(self, flags=0):
        # :api
        """Factory function returning a DNF Query."""
        return dnf.query.Query(self, flags)


def _build_sack(base):
    cachedir = base.conf.cachedir
    # create the dir ourselves so we have the permissions under control:
    dnf.util.ensure_dir(cachedir)
    return Sack(pkgcls=dnf.package.Package, pkginitval=base,
                arch=base.conf.substitutions["arch"],
                cachedir=cachedir, rootdir=base.conf.installroot,
                logfile=os.path.join(base.conf.logdir, dnf.const.LOG_HAWKEY),
                logdebug=base.conf.logfilelevel > 9)


def _rpmdb_sack(base):
    # used by subscription-manager (src/dnf-plugins/product-id.py)
    sack = _build_sack(base)
    try:
        # It can fail if rpmDB is not present
        sack.load_system_repo(build_cache=False)
    except IOError:
        pass
    return sack


def rpmdb_sack(base):
    # :api
    """
    Returns a new instance of sack containing only installed packages (@System repo)
    Useful to get list of the installed RPMs after transaction.
    """
    return _rpmdb_sack(base)
