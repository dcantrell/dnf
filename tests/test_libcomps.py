# -*- coding: utf-8 -*-

# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import

import libcomps

import tests.support


class LibcompsTest(tests.support.TestCase):

    """Sanity tests of the Libcomps library."""

    def test_environment_parse(self):
        xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE comps PUBLIC "-//Red Hat, Inc.//DTD Comps info//EN" "comps.dtd">
<comps>
  <group>
   <id>somerset</id>
   <default>true</default>
   <uservisible>true</uservisible>
   <display_order>1024</display_order>
   <name>Solid Ground</name>
   <description>--</description>
    <packagelist>
      <packagereq type="mandatory">pepper</packagereq>
      <packagereq type="mandatory">trampoline</packagereq>
    </packagelist>
  </group>
  <environment>
    <id>minimal</id>
    <name>Min install</name>
    <description>Basic functionality.</description>
    <display_order>5</display_order>
    <grouplist>
      <groupid>somerset</groupid>
    </grouplist>
  </environment>
</comps>
"""
        comps = libcomps.Comps()
        ret = comps.fromxml_str(xml)
        self.assertGreaterEqual(ret, 0)

    def test_segv(self):
        c1 = libcomps.Comps()
        c2 = libcomps.Comps()
        c2.fromxml_f(tests.support.COMPS_PATH)
        c1 + c2  # sigsegved here

    def test_segv2(self):
        c1 = libcomps.Comps()
        c1.fromxml_f(tests.support.COMPS_PATH)

        c2 = libcomps.Comps()
        c2.fromxml_f(tests.support.COMPS_PATH)

        c = c1 + c2
        c.groups[0].packages[0].name
