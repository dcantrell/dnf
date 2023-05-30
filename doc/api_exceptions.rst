..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

============
 Exceptions
============

.. exception:: dnf.exceptions.Error

  Base class for all DNF Errors.

.. exception:: dnf.exceptions.CompsError

  Used for errors of comps groups like trying to work with group which is not available.

.. exception:: dnf.exceptions.DeprecationWarning

  Used to emit deprecation warnings using Python's :func:`warnings.warning` function.

.. exception:: dnf.exceptions.DepsolveError

  Error during transaction dependency resolving.

.. exception:: dnf.exceptions.DownloadError

  Error during downloading packages from the repositories.

.. exception:: dnf.exceptions.MarkingError

  Error when DNF was unable to find a match for given package / group / module specification.

.. exception:: dnf.exceptions.MarkingErrors

  Categorized errors during processing of the request. The available error categories are ``no_match_pkg_specs`` for missing packages, ``error_pkg_specs`` for broken packages, ``no_match_group_specs`` for missing groups or modules, ``error_group_specs`` for broken groups or modules and ``module_depsolv_errors`` for modular dependency problems.

.. exception:: dnf.exceptions.RepoError

  Error when loading repositories.
