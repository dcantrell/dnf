..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

===============
 Configuration
===============

Configurable settings of the :class:`dnf.Base` object are stored into a :class:`dnf.conf.Conf` instance. The various options are described here.

.. class:: dnf.conf.Conf

    This object has attributes corresponding to all configuration options from both :ref:`"[main] Options" <conf_main_options-label>` and :ref:`"Options for both [main] and Repo" <conf_main_and_repo_options-label>` sections. For example setting a proxy to access all repositories::

        import dnf

        base = dnf.Base()
        conf = base.conf
        conf.proxy = "http://the.proxy.url:3128"
        conf.proxy_username = "username"
        conf.proxy_password = "secret"
        base.read_all_repos()
        base.fill_sack()


  .. attribute:: get_reposdir

    Returns the value of the first valid reposdir or if unavailable the value of created reposdir (string)

  .. attribute:: substitutions

    An instance of :class:`dnf.conf.substitutions.Substitutions` class. A mapping of substitutions used in repositories' remote URL configuration. The commonly used ones are:

    ==========     ============================================== ============
    key            meaning                                        default
    ==========     ============================================== ============
    arch           architecture of the machine                    autodetected
    basearch       the architecture family of the current "arch"  autodetected
    releasever     release name of the system distribution        ``None``
    ==========     ============================================== ============

    :func:`dnf.rpm.detect_releasever` can be used to detect the ``releasever`` value.

    Following example shows recommended method how to override autodetected architectures::

        import dnf
        import hawkey

        arch = hawkey.detect_arch()
        base = dnf.Base()
        base.conf.substitutions['arch'] = arch
        base.conf.substitutions['basearch'] = dnf.rpm.basearch(arch)
        base.fill_sack()
        ...


  .. method:: exclude_pkgs(pkgs)

    Exclude all packages in the `pkgs` list from all operations.

  .. method:: prepend_installroot(option)

    Prefix config option named `option` with :attr:`installroot`.

  .. method:: read(filename=None)

    Read configuration options from the ``main`` section in `filename`. Option values not present there are left at their current values. If `filename` is ``None``, :attr:`config_file_path` is used. Conversely, the configuration path used to load the configuration file that was used is stored into :attr:`config_file_path` before the function returns.

  .. method:: dump()

    Print configuration values, including inherited values.

  .. method:: set_or_append_opt_value(name, value_string, priority=PRIO_RUNTIME).

    For standard options, sets the value of the option if the `priority` is equal to or higher
    than the current priority.
    For "append" options, appends the values parsed from `value_string` to the current list of values. If the first
    parsed element of the list of values is empty and the `priority` is equal to or higher than the current
    priority, the current list is replaced with the new values.
    If the `priority` is higher than the current priority, the current priority is increased to the `priority`.
    Raises :exc:`dnf.exceptions.ConfigError` if the option with the given `name` does not exist or `value_string` contains
    an invalid value or not allowed value.


  .. method:: write_raw_configfile(filename, section_id, substitutions, modify)

    Update or create config file. Where `filename` represents name of config file (.conf or .repo); `section_id`
    represents id of modified section (e.g. main, fedora, updates); `substitutions` represents an instance of
    base.conf.substitutions; `modify` represents dict of modified options.


.. class:: dnf.conf.substitutions.Substitutions

  .. method:: update_from_etc(installroot, varsdir=("/etc/yum/vars/", "/etc/dnf/vars/"))

    Read user-defined variables values from variable directories. See :ref:`variable files <varfiles-label>` in Configuration reference.
