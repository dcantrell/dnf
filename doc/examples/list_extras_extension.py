# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

"""An extension that lists installed packages not available
   in any remote repository.
"""

import dnf


if __name__ == '__main__':

    with dnf.Base() as base:
        # Repositories serve as sources of information about packages.
        base.read_all_repos()
        # A sack is needed for querying.
        base.fill_sack()

        # A query matches all packages in sack
        q = base.sack.query()

        # Derived query matches only available packages
        q_avail = q.available()
        # Derived query matches only installed packages
        q_inst = q.installed()

        available = q_avail.run()
        for pkg in q_inst.run():
            if pkg not in available:
                print(str(pkg))
