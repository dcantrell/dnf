# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

import locale
import os

# run tests with C locales
os.environ["LC_ALL"] = "C.UTF-8"
os.environ["LANG"] = "C.UTF-8"
os.environ["LANGUAGE"] = "en_US:en"
locale.setlocale(locale.LC_ALL, "C.UTF-8")
