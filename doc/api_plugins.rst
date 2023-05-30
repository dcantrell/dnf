..
  Copyright The dnf Project Authors
  SPDX-License-Identifier: GPL-2.0-or-later

==================
 Plugin Interface
==================

DNF plugin can be any Python class fulfilling the following criteria:

1. it derives from :class:`dnf.Plugin`,
2. it is made available in a Python module stored in one of the :attr:`.Conf.pluginpath`,
3. provides its own :attr:`~.Plugin.name` and :meth:`~.Plugin.__init__`.

When DNF CLI runs it loads the plugins found in the paths during the CLI's initialization.

.. class:: dnf.Plugin

  The base class all DNF plugins must derive from.

  .. attribute:: name

    The plugin must set this class variable to a string identifying the plugin. The string can only contain alphanumeric characters and underscores.

  .. staticmethod:: read_config(conf)

    Read plugin's configuration into a `ConfigParser <http://docs.python.org/3/library/configparser.html>`_ compatible instance. `conf` is a :class:`.Conf` instance used to look up the plugin configuration directory.

  .. method:: __init__(base, cli)

    The plugin must override this. Called immediately after all the plugins are loaded. `base` is an instance of :class:`dnf.Base`. `cli` is an instance of :class:`dnf.cli.Cli` but can also be ``None`` in case DNF is running without a CLI (e.g. from an extension).

  .. method:: pre_config()

    This hook is called before configuring the repos.

  .. method:: config()

    This hook is called immediately after the CLI/extension is finished configuring DNF.  The plugin can use this to tweak the global configuration or the repository configuration.

  .. method:: resolved()

    This hook is called immediately after the CLI has finished resolving a transaction. The plugin can use this to inspect the resolved but not yet executed :attr:`Base.transaction`.

  .. method:: sack()

    This hook is called immediately after :attr:`.Base.sack` is initialized with data from all the enabled repos.

  .. method:: pre_transaction()

    This hook is called just before transaction execution. This means after a successful transaction test. RPMDB is locked during that time.

  .. method:: transaction()

    This hook is called immediately after a successful transaction.
    Plugins that were removed or obsoleted by the transaction will not run the transaction hook.

.. method:: register_command(command_class)

    A class decorator for automatic command registration.

    Example of a plugin that provides a hello-world dnf command (the file must be placed in one of the :ref:`pluginpath <pluginpath-label>` directories::

        import dnf

        @dnf.plugin.register_command
        class HelloWorldCommand(dnf.cli.Command):
            aliases = ('hello-world',)
            summary = 'The example command'

            def run(self):
                print('Hello world!')

    To run the command::

        $ dnf hello-world
        Hello world!


You may want to see the comparison with `yum plugin hook API`_.

.. _yum plugin hook API: https://dnf.readthedocs.io/en/latest/api_vs_yum.html
