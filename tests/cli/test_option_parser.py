# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import argparse

from dnf.cli.option_parser import OptionParser

import dnf.cli.commands
import dnf.pycomp
import dnf.util

import tests.support
from tests.support import mock


def _parse(command, args):
    parser = OptionParser()
    opts = parser.parse_main_args(args)
    opts = parser.parse_command_args(command, args)
    return parser, opts


class OptionParserTest(tests.support.TestCase):
    def setUp(self):
        self.cli = mock.Mock()
        self.command = MyTestCommand(self.cli)

    def test_parse(self):
        parser, opts = _parse(self.command, ['update', '--nogpgcheck'])
        self.assertEqual(opts.command, 'update')
        self.assertFalse(opts.gpgcheck)
        self.assertIsNone(opts.color)


class MyTestCommand(dnf.cli.commands.Command):

    aliases = ["test-cmd"]
    summary = 'summary'

    def __init__(self, cli):
        dnf.cli.commands.Command.__init__(self, cli)


class MyTestCommand2(dnf.cli.commands.Command):

    aliases = ["test-cmd2"]
    summary = 'summary2'

    def __init__(self, cli):
        dnf.cli.commands.Command.__init__(self, cli)


class OptionParserAddCmdTest(tests.support.TestCase):

    def setUp(self):
        self.cli_commands = {}
        self.parser = OptionParser()
        self.parser._ = dnf.pycomp.NullTranslations().ugettext
        self.cli = mock.Mock()

    def _register_command(self, command_cls):
        """ helper for simulate dnf.cli.cli.Cli.register_Command()"""
        for name in command_cls.aliases:
            self.cli_commands[name] = command_cls

    def test_add_commands(self):
        cmd = MyTestCommand(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "main")
        name = cmd.aliases[0]
        self.assertTrue(name in self.parser._cmd_usage)
        group, summary = self.parser._cmd_usage[name]
        self.assertEqual(group, 'main')
        self.assertEqual(summary, cmd.summary)
        self.assertEqual(self.parser._cmd_groups, set(['main']))

    def test_add_commands_only_once(self):
        cmd = MyTestCommand(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "main")
        cmd = MyTestCommand(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "plugin")
        self.assertEqual(len(self.parser._cmd_usage.keys()), 1)
        self.assertEqual(self.parser._cmd_groups, set(['main']))

    def test_cmd_groups(self):
        cmd = MyTestCommand(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "main")
        cmd = MyTestCommand2(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "plugin")
        self.assertEqual(len(self.parser._cmd_groups), 2)
        self.assertEqual(self.parser._cmd_groups, set(['main', 'plugin']))

    def test_help_option_set(self):
        opts = self.parser.parse_main_args(['-h'])
        self.assertTrue(opts.help)

    def test_help_option_notset(self):
        opts = self.parser.parse_main_args(['foo', 'bar'])
        self.assertFalse(opts.help)

    def test_get_usage(self):
        parser = argparse.ArgumentParser()
        output = [
            u'%s [options] COMMAND' % (parser.prog if parser.prog in ["dnf", "yum"] else "dnf"),
            u'',
            u'List of Main Commands:',
            u'',
            u'test-cmd                  summary',
            u'',
            u'List of Plugin Commands:',
            u'',
            u'test-cmd2                 summary2',
            u'']
        cmd = MyTestCommand(self.cli)
        self._register_command(cmd)
        self.parser.add_commands(self.cli_commands, "main")
        cmd2 = MyTestCommand2(self.cli)
        self._register_command(cmd2)
        self.parser.add_commands(self.cli_commands, "plugin")
        self.assertEqual(len(self.parser._cmd_usage.keys()), 2)
        usage = self.parser.get_usage().split('\n')
        self.assertEqual(usage, output)
