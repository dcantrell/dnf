# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

"""An extension that ensures that given features are present."""


import sys

import dnf
import dnf.module
import dnf.rpm


if __name__ == '__main__':
    FTR_SPECS = {'acpi-1.7-10.fc29.x86_64'}  # <-- SET YOUR FEATURES HERE.
    RPM_SPECS = {'./acpi-1.7-10.fc29.x86_64.rpm'}  # <-- SET YOUR RPMS HERE.
    GRP_SPECS = {'kde-desktop'}  # <-- SET YOUR GROUPS HERE.
    MODULE_SPEC = {"nodejs:10/default"}  # <-- SET YOUR MODULES HERE.

    with dnf.Base() as base:
        # Substitutions are needed for correct interpretation of repo files.
        RELEASEVER = dnf.rpm.detect_releasever(base.conf.installroot)
        base.conf.substitutions['releasever'] = RELEASEVER
        # Repositories are needed if we want to install anything.
        base.read_all_repos()
        # A sack is required by marking methods and dependency resolving.
        base.fill_sack()
        # Feature marking methods set the user request.
        for ftr_spec in FTR_SPECS:
            try:
                base.install(ftr_spec)
            except dnf.exceptions.MarkingError:
                sys.exit('Feature(s) cannot be found: ' + ftr_spec)
        # Package marking methods set the user request.
        for pkg in base.add_remote_rpms(RPM_SPECS, strict=False):
            try:
                base.package_install(pkg, strict=False)
            except dnf.exceptions.MarkingError:
                sys.exit('RPM cannot be found: ' + pkg)
        # Comps data reading initializes the base.comps attribute.
        if GRP_SPECS:
            base.read_comps(arch_filter=True)
        # Group marking methods set the user request.
        if MODULE_SPEC:
            module_base = dnf.module.module_base.ModuleBase(base)
            module_base.install(MODULE_SPEC, strict=False)
        for grp_spec in GRP_SPECS:
            group = base.comps.group_by_pattern(grp_spec)
            if not group:
                sys.exit('Group cannot be found: ' + grp_spec)
            base.group_install(group.id, ['mandatory', 'default'])
        # Resolving finds a transaction that allows the packages installation.
        try:
            base.resolve()
        except dnf.exceptions.DepsolveError:
            sys.exit('Dependencies cannot be resolved.')
        # The packages to be installed must be downloaded first.
        try:
            base.download_packages(base.transaction.install_set)
        except dnf.exceptions.DownloadError:
            sys.exit('Required package cannot be downloaded.')
        # The request can finally be fulfilled.
        base.do_transaction()
