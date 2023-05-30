# pycomp.py
# Python 2 and Python 3 compatibility module
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from gettext import NullTranslations
from sys import version_info
import base64
import email.mime.text
import gettext
import itertools
import locale
import sys
import types

PY3 = version_info.major >= 3

if PY3:
    from io import StringIO
    from configparser import ConfigParser
    import queue
    import urllib.parse
    import shlex

    # functions renamed in py3
    Queue = queue.Queue
    basestring = unicode = str
    filterfalse = itertools.filterfalse
    long = int
    NullTranslations.ugettext = NullTranslations.gettext
    NullTranslations.ungettext = NullTranslations.ngettext
    xrange = range
    raw_input = input
    base64_decodebytes = base64.decodebytes
    urlparse = urllib.parse
    urllib_quote = urlparse.quote
    shlex_quote = shlex.quote
    sys_maxsize = sys.maxsize


    def gettext_setup(t):
        _ = t.gettext
        P_ = t.ngettext
        return (_, P_)

    # string helpers
    def is_py2str_py3bytes(o):
        return isinstance(o, bytes)
    def is_py3bytes(o):
        return isinstance(o, bytes)

    # functions that don't take unicode arguments in py2
    ModuleType = lambda m: types.ModuleType(m)
    format = locale.format_string
    def setlocale(category, loc=None):
        locale.setlocale(category, loc)
    def write_to_file(f, content):
        f.write(content)
    def email_mime(body):
        return email.mime.text.MIMEText(body)
else:
    # functions renamed in py3
    from __builtin__ import unicode, basestring, long, xrange, raw_input
    from StringIO import StringIO
    from ConfigParser import ConfigParser
    import Queue
    import urllib
    import urlparse
    import pipes

    Queue = Queue.Queue
    filterfalse = itertools.ifilterfalse
    base64_decodebytes = base64.decodestring
    urllib_quote = urllib.quote
    shlex_quote = pipes.quote
    sys_maxsize = sys.maxint

    def gettext_setup(t):
        _ = t.ugettext
        P_ = t.ungettext
        return (_, P_)

    # string helpers
    def is_py2str_py3bytes(o):
        return isinstance(o, str)
    def is_py3bytes(o):
        return False

    # functions that don't take unicode arguments in py2
    ModuleType = lambda m: types.ModuleType(m.encode('utf-8'))
    def format(percent, *args, **kwargs):
        return locale.format(percent.encode('utf-8'), *args, **kwargs)
    def setlocale(category, loc=None):
        locale.setlocale(category, loc.encode('utf-8'))
    def write_to_file(f, content):
        f.write(content.encode('utf-8'))
    def email_mime(body):
        return email.mime.text.MIMEText(body.encode('utf-8'))
