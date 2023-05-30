..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

===========
Transaction
===========

.. module:: dnf.db.group


.. class:: RPMTransaction

  Instances of this class describe a resolved transaction set. The transaction object can be iterated for the contained :class:`items <.TransactionItem>`.

  The packaging requests from the contained items are later passed to the core package manager (RPM) as they are without further dependency resolving. If the set is not fit for an actual transaction (e.g. introduces conflicts, has inconsistent dependencies) RPM then by default refuses to proceed.

  .. attribute:: install_set

    Read-only property which contains set of :class:`Packages <.package.Package>` to be installed.

  .. attribute:: remove_set

    Read-only property which contains set of :class:`Packages <.package.Package>` to be removed.
