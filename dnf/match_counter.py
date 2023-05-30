# match_counter.py
# Implements class MatchCounter.
#
# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later
#

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from functools import reduce

WEIGHTS = {
    'name'		: 7,
    'summary'		: 4,
    'description'	: 2,
    'url'		: 1,
    }


def _canonize_string_set(sset, length):
    """ Ordered sset with empty strings prepended. """
    current = len(sset)
    l = [''] * (length - current) + sorted(sset)
    return l


class MatchCounter(dict):
    """Map packages to which of their attributes matched in a search against
    what values.

    The mapping is: ``package -> [(key, needle), ... ]``.

    """

    @staticmethod
    def _eval_weights(pkg, matches):
        # how much is each match worth and return their sum:
        def weight(match):
            key = match[0]
            needle = match[1]
            haystack = getattr(pkg, key)
            if key == "name" and haystack == needle:
                # if package matches exactly by name, increase weight
                return 2 * WEIGHTS[key]
            return WEIGHTS[key]

        return sum(map(weight, matches))

    def _key_func(self):
        """Get the key function used for sorting matches.

        It is not enough to only look at the matches and order them by the sum
        of their weighted hits. In case this number is the same we have to
        ensure that the same matched needles are next to each other in the
        result.

        Returned function is:
        pkg -> (weights_sum, canonized_needles_set, -distance)

        """
        def get_key(pkg):
            return (
                # use negative value to make sure packages with the highest weight come first
                - self._eval_weights(pkg, self[pkg]),
                # then order packages alphabetically
                pkg.name,
            )
        return get_key

    def _max_needles(self):
        """Return the max count of needles of all packages."""
        if self:
            return max(len(self.matched_needles(pkg)) for pkg in self)
        return 0

    def add(self, pkg, key, needle):
        self.setdefault(pkg, []).append((key, needle))

    def dump(self):
        for pkg in self:
            print('%s\t%s' % (pkg, self[pkg]))

    def matched_haystacks(self, pkg):
        return set(getattr(pkg, m[0]) for m in self[pkg])

    def matched_keys(self, pkg):
        # return keys in the same order they appear in the list
        result = []
        for i in self[pkg]:
            if i[0] in result:
                continue
            result.append(i[0])
        return result

    def matched_needles(self, pkg):
        return set(m[1] for m in self[pkg])

    def sorted(self, reverse=False, limit_to=None):
        keys = limit_to if limit_to else self.keys()
        return sorted(keys, key=self._key_func())

    def total(self):
        return reduce(lambda total, pkg: total + len(self[pkg]), self, 0)
