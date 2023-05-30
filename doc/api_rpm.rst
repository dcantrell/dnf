..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

===============
 RPM Interface
===============

.. module:: dnf.rpm

.. function:: detect_releasever(installroot)

  Return the release name of the distribution of the tree rooted at `installroot`. The function uses information from RPMDB found under the tree.

  Returns ``None`` if the information can not be determined (perhaps because the tree has no RPMDB).

.. function:: basearch(arch)

  Return base architecture of the processor based on `arch` type given. E.g. when `arch` i686 is given then the returned value will be i386.
