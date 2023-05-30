# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import
from __future__ import unicode_literals

import os
from io import StringIO

import dnf.cli.cli

import tests.support
from tests.support import mock

'''
def _run(cli, args):
    with mock.patch('sys.stdout', new_callable=StringIO), \
            mock.patch('dnf.rpm.detect_releasever', return_value=69):
        cli.configure(['clean', '--config', '/dev/null'] + args)
        cli.run()


class CleanTest(tests.support.TestCase):
    def setUp(self):
        conf = dnf.conf.Conf()
        base = tests.support.Base(conf)
        base.repos.add(tests.support.MockRepo('main', conf))
        base.conf.reposdir = '/dev/null'
        base.conf.plugins = False
        base.output = tests.support.MockOutput()

        repo = base.repos['main']
        repo.baseurl = ['http:///dnf-test']
        repo.basecachedir = base.conf.cachedir

        walk = [
            (
                repo.basecachedir,
                [os.path.basename(repo._cachedir)],
                [repo.id + '.solv'],
            ),
            (repo._cachedir, ['repodata', 'packages'], ['metalink.xml']),
            (repo._cachedir + '/repodata', [], ['foo.xml', 'bar.xml.bz2']),
            (repo._cachedir + '/packages', [], ['foo.rpm']),
        ]
        os.walk = self.walk = mock.Mock(return_value=walk)
        self.base = base
        self.cli = dnf.cli.cli.Cli(base)

    def tearDown(self):
        self.base.close()

    def test_run(self):
        with mock.patch('dnf.cli.commands.clean._clean') as _clean:
            for args in [['all'],
                         ['metadata'],
                         ['metadata', 'packages'],
                         ['metadata', 'packages', 'expire-cache'],
                         ['dbcache'],
                         ['expire-cache']]:
                _run(self.cli, args)

        calls = [call[0] for call in _clean.call_args_list]
        counts = (5, 4, 5, 5, 1, 0)
        for call, count in zip(calls, counts):
            files = list(call[1])
            assert len(files) == count

    def test_walk_once(self):
        _run(self.cli, ['all'])
        assert len(self.walk.call_args_list) == 1

    def test_clean_local_repo(self):
        cachedir = self.base.conf.cachedir
        repo = self.base.repos['main']
        repo.baseurl = ['file:///localrepo']

        _run(self.cli, ['all'])

        # Make sure we never looked outside the base cachedir
        dirs = [call[0][0] for call in self.walk.call_args_list]
        assert all(d == cachedir for d in dirs)
'''
