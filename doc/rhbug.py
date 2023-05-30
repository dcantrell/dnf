# rhbug.py
# rhbug Sphinx extension.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from docutils import nodes

try:
    import bugzilla
except ImportError:
    bugzilla = None
import json
import os

class Summary(object):
    def __init__(self, cache_fn):
        self.cache_fn = cache_fn

    def __call__(self, bug_id):
        bug_id = int(bug_id)
        summary = self._from_cache(bug_id)
        if summary is not None:
            return summary
        summary = self._from_bugzilla(bug_id)
        self._store_in_cache(bug_id, summary)
        return summary

    def _from_bugzilla(self, bug_id):
        if bugzilla is None:
            return ''
        rhbz = bugzilla.RHBugzilla(url="https://bugzilla.redhat.com/xmlrpc.cgi")
        query = rhbz.build_query(bug_id=bug_id)
        bug = rhbz.query(query)[0]
        return bug.summary

    def _from_cache(self, bug_id):
        try:
            with open(self.cache_fn, 'r') as json_file:
                cache = json.load(json_file)
                summary = [entry[1] for entry in cache if entry[0] == bug_id]
                return summary[0]
        except (IOError, IndexError):
            return None

    def _store_in_cache(self, bug_id, summary):
        if bugzilla is None:
            return
        try:
            with open(self.cache_fn, 'r') as json_file:
                cache = json.load(json_file)
        except IOError:
            cache = []
        cache.append((bug_id, summary))
        with open(self.cache_fn, 'w') as json_file:
            json.dump(cache, json_file, indent=4)

def RhBug_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    source = inliner.document.settings._source
    summaries_fn = '%s/summaries_cache' % os.path.dirname(source)
    summary = Summary(summaries_fn)(text)
    link_name = 'Bug %s - %s' % (text, summary)
    url = 'https://bugzilla.redhat.com/show_bug.cgi?id=%s' % text
    node = nodes.reference(rawtext, link_name, refuri=url)
    return [node], []

def setup(app):
    app.add_role('rhbug', RhBug_role)
