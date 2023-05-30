..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

###################################
 Changes in DNF-2 compared to DNF-1
###################################

=============
 CLI changes
=============

Reintroduction of YUM's configuration options ``includepkgs`` and ``excludepkgs``
===================================================================================

Due to a better compatibility with YUM, configuration options ``include`` and ``exclude``
were replaced by the original options :ref:`includepkgs <include-label>` and
:ref:`excludepkgs <exclude-label>`.

DNF group install ``--with-optional`` option
============================================

Installation of optional packages of group is changed from subcommand
``with-optional`` to option ``--with-optional``.

==================
Python API changes
==================

All non-API methods and attributes are private
==============================================

.. warning:: All non-API methods and attributes of :doc:`documented modules <api>` are now private
             in order to accomplish more distinguishable API.

Following API methods accept different arguments
================================================

#. :meth:`dnf.Base.add_remote_rpms`
#. :meth:`dnf.Base.group_install`
#. :meth:`dnf.cli.Command.configure`
#. :meth:`dnf.cli.Command.run`
#. :meth:`dnf.Plugin.read_config`
