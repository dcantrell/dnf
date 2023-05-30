# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import dnf.logging
import dnf.plugin
import dnf.pycomp

import tests.support


PLUGINS = "%s/tests/plugins" % tests.support.dnf_toplevel()


def testconf():
    conf = tests.support.FakeConf()
    conf.pluginpath = [PLUGINS]
    conf.pluginconfpath = [PLUGINS]
    return conf


class PluginTest(tests.support.TestCase):
    def setUp(self):
        self.plugins = dnf.plugin.Plugins()
        self.plugins._load(testconf(), (), ())

    def tearDown(self):
        self.plugins._unload()

    def test_load(self):
        self.assertLength(self.plugins.plugin_cls, 1)
        cls = self.plugins.plugin_cls[0]
        assert(issubclass(cls, dnf.plugin.Plugin))
        self.assertEqual(cls.name, 'lucky')

    def test_runs(self):
        self.assertLength(self.plugins.plugins, 0)
        self.plugins._run_init(None, None)
        self.assertLength(self.plugins.plugins, 1)
        self.plugins._run_config()
        lucky = self.plugins.plugins[0]
        self.assertTrue(lucky._config)

    def test_config(self):
        base = tests.support.MockBase()
        base.conf.pluginconfpath = ['/wrong', PLUGINS]
        self.plugins._run_init(base, None)
        lucky = self.plugins.plugins[0]
        conf = lucky.read_config(base.conf)
        self.assertTrue(conf.getboolean('main', 'enabled'))
        self.assertEqual(conf.get('main', 'wanted'), '/to/be/haunted')
        base.close()

    def test_disabled(self):
        base = tests.support.MockBase()
        base.conf.pluginconfpath = [PLUGINS]
        self.plugins._run_init(base, None)
        self.assertFalse(any([p.name == 'disabled-plugin'
                              for p in self.plugins.plugins]))
        self.assertLength(self.plugins.plugin_cls, 1)
        self.assertEqual(self.plugins.plugin_cls[0].name, 'lucky')
        base.close()


class PluginSkipsTest(tests.support.TestCase):
    def test_skip(self):
        self.plugins = dnf.plugin.Plugins()
        self.plugins._load(testconf(), ('luck*',), ())
        self.assertLength(self.plugins.plugin_cls, 0)

    def tearDown(self):
        self.plugins._unload()


class PluginNonExistentTest(tests.support.TestCase):

    """Tests with a non-existent plugin."""

    def test_logs_traceback(self):
        """Test whether the traceback is logged if a plugin cannot be imported."""
        package = dnf.pycomp.ModuleType('testpkg')
        package.__path__ = []
        stream = dnf.pycomp.StringIO()

        with tests.support.wiretap_logs('dnf', dnf.logging.SUBDEBUG, stream):
            dnf.plugin._import_modules(package, ('nonexistent.py',))

        end = ('Error: No module named \'testpkg\'\n' if dnf.pycomp.PY3
               else 'Error: No module named testpkg.nonexistent\n')
        self.assertTracebackIn(end, stream.getvalue())
