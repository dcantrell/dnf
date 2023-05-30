# Copyright The dnf Project Authors
# SPDX-License-Identifier: GPL-2.0-or-later

from dnf.i18n import _

DIFFERENT_STREAM_INFO = 1
NOTHING_TO_SHOW = 2
INSTALLING_NEWER_VERSION = 4
ENABLED_MODULES = 5
NO_PROFILE_SPECIFIED = 6

module_messages = {
    DIFFERENT_STREAM_INFO: _("Enabling different stream for '{}'."),
    NOTHING_TO_SHOW: _("Nothing to show."),
    INSTALLING_NEWER_VERSION: _("Installing newer version of '{}' than specified. Reason: {}"),
    ENABLED_MODULES: _("Enabled modules: {}."),
    NO_PROFILE_SPECIFIED: _("No profile specified for '{}', please specify profile."),
}
