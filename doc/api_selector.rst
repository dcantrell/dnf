..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

==========
 Selector
==========

.. class:: dnf.selector.Selector

  Specify a target of a transaction operation.

  .. method:: set

    Set content of Selector similarly like :meth:`dnf.query.Query.filter`

  .. method:: matches

    Returns packages that represents the content of Selector
