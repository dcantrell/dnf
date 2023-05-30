..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

======
 Sack
======

.. module:: dnf.sack

.. class:: Sack

  The package sack. Contains metadata information about all known packages, installed and available.

  .. method:: query(flags=hawkey.APPLY_EXCLUDES)

    Return a :class:`Query<dnf.query.Query>` for querying packages contained in this sack.

    :ref:`Package filtering <excluded_packages-label>` is applied when creating the query object. The behavior can be adapted using flags. Possible flags:


    ==============================   ===========================================================================
    Flag                             Value meaning
    ==============================   ===========================================================================
    hawkey.APPLY_EXCLUDES            Apply all package filtering.
    hawkey.IGNORE_EXCLUDES           Ignore all package filtering.
    hawkey.IGNORE_REGULAR_EXCLUDES   Ignore regular excludes defined by configuration files or the command line.
    hawkey.IGNORE_MODULAR_EXCLUDES   Ignore modular filtering.
    ==============================   ===========================================================================

.. function:: rpmdb_sack(base)

    Returns a new instance of sack containing only installed packages (@System repo). Useful to get list of the installed RPMs after transaction.
